import pandas as pd
import sqlite3
from datetime import datetime

print("Creating SQLite database...")

# Create database connection
conn = sqlite3.connect('data/job_market.db')
cursor = conn.cursor()

# Create jobs table with our schema
print("\nCreating jobs table...")
cursor.execute('''
CREATE TABLE IF NOT EXISTS jobs (
    job_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    company_name TEXT,
    location TEXT,
    description TEXT,
    posted_at TEXT,
    salary_min REAL,
    salary_max REAL,
    work_type TEXT,
    source TEXT,
    url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

print("Table created successfully!")

# Load the combined CSV
print("\nLoading data from CSV...")
df = pd.read_csv('data/processed/jobs_combined.csv')
print(f"Loaded {len(df):,} rows")

# Insert data into database
print("\nInserting data into database...")
df.to_sql('jobs', conn, if_exists='replace', index=False)
print("Data inserted successfully!")

# Verify the data
print("\n" + "="*50)
print("DATABASE VERIFICATION")
print("="*50)

# Count total rows
cursor.execute("SELECT COUNT(*) FROM jobs")
total_rows = cursor.fetchone()[0]
print(f"\nTotal rows in database: {total_rows:,}")

# Count by source
print("\nRows by source:")
cursor.execute("SELECT source, COUNT(*) as count FROM jobs GROUP BY source ORDER BY count DESC")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]:,}")

# Count by work type
print("\nRows by work type:")
cursor.execute("SELECT work_type, COUNT(*) as count FROM jobs GROUP BY work_type ORDER BY count DESC")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]:,}")

# Jobs with salary data
cursor.execute("SELECT COUNT(*) FROM jobs WHERE salary_min IS NOT NULL")
with_salary = cursor.fetchone()[0]
print(f"\nJobs with salary data: {with_salary:,} ({with_salary/total_rows*100:.1f}%)")

# Top companies
print("\nTop 10 companies by job count:")
cursor.execute("SELECT company_name, COUNT(*) as count FROM jobs GROUP BY company_name ORDER BY count DESC LIMIT 10")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]:,}")

# Sample query
print("\nSample jobs (first 5):")
cursor.execute("SELECT job_id, title, company_name, location, work_type FROM jobs LIMIT 5")
for row in cursor.fetchall():
    print(f"  ID {row[0]}: {row[1]} at {row[2]} ({row[3]}) - {row[4]}")

# Close connection
conn.close()

print("\n" + "="*50)
print("✅ Database created successfully!")
print("📁 Location: data/job_market.db")
print("📊 Ready to connect to Tableau!")
print("="*50)

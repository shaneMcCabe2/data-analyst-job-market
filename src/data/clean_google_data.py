import pandas as pd
import re
from datetime import datetime, timedelta

print("Loading Google Search data...")
df = pd.read_csv('data-analyst-job-postings-google-search/gsearch_jobs.csv')
print(f"Original rows: {len(df):,}")

# 1. Filter for USA jobs
print("\nFiltering for USA jobs...")
df_usa = df[df['location'].notna()].copy()
non_usa_keywords = ['Canada', 'London', 'India', 'Australia']
for keyword in non_usa_keywords:
    df_usa = df_usa[~df_usa['location'].str.contains(keyword, case=False, na=False)]
print(f"After USA filter: {len(df_usa):,} rows")

# 2. Clean whitespace in location
print("\nCleaning whitespace...")
df_usa['location'] = df_usa['location'].str.strip()
print("Top locations after cleaning:")
print(df_usa['location'].value_counts().head(5))

# 3. Standardize remote/anywhere jobs
print("\nStandardizing remote locations...")
df_usa['is_remote'] = df_usa['location'].str.contains('Anywhere', case=False, na=False)
df_usa.loc[df_usa['is_remote'], 'location'] = 'Remote - USA'
print(f"Remote jobs: {df_usa['is_remote'].sum():,}")

# 4. Select and rename columns for our schema
print("\nMapping to unified schema...")
df_clean = pd.DataFrame({
    'title': df_usa['title'],
    'company_name': df_usa['company_name'],
    'location': df_usa['location'],
    'description': df_usa['description'],
    'posted_at': df_usa['posted_at'],
    'salary_min': df_usa['salary_min'],
    'salary_max': df_usa['salary_max'],
    'work_type': df_usa['work_from_home'].apply(
        lambda x: 'Remote' if x == True else ('Onsite' if x == False else 'Not Specified')
    ),
    'source': 'Google Search',
    'url': None
})

print(f"\nFinal cleaned rows: {len(df_clean):,}")

print("\nWork type distribution:")
print(df_clean['work_type'].value_counts())

print("\nSalary data completeness:")
print(f"Has salary: {df_clean['salary_min'].notna().sum():,} ({df_clean['salary_min'].notna().sum()/len(df_clean)*100:.1f}%)")

print("\nSaving cleaned data...")
df_clean.to_csv('data/processed/google_search_cleaned.csv', index=False)
print("Saved to data/processed/google_search_cleaned.csv")
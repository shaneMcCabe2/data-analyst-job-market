import pandas as pd

print("Loading LinkedIn Data Jobs dataset...")
df = pd.read_csv('linkedin-data-jobs-dataset/clean_jobs.csv')
print(f"Original rows: {len(df):,}")

# 1. Filter for USA jobs only
print("\nFiltering for USA jobs...")
df_usa = df[df['location'].notna()].copy()

# Filter out non-USA locations
non_usa_keywords = ['Canada', 'London', 'India', 'Australia', 'United Kingdom', 'Singapore', 'Germany']
for keyword in non_usa_keywords:
    df_usa = df_usa[~df_usa['location'].str.contains(keyword, case=False, na=False)]

print(f"After USA filter: {len(df_usa):,} rows")

# Show sample locations
print("\nSample locations:")
print(df_usa['location'].value_counts().head(10))

# 2. Clean location data
print("\nCleaning locations...")
df_usa['location'] = df_usa['location'].str.strip()

# 3. Map to unified schema
print("\nMapping to unified schema...")
df_clean = pd.DataFrame({
    'title': df_usa['title'],
    'company_name': df_usa['company'],
    'location': df_usa['location'],
    'description': df_usa['description'],
    'posted_at': df_usa['date_posted'],
    'salary_min': None,
    'salary_max': None,
    'work_type': 'Not Specified',  # This field was 100% null
    'source': 'LinkedIn',
    'url': df_usa['link']
})

print(f"\nFinal cleaned rows: {len(df_clean):,}")

# Stats
print("\nSample of cleaned data:")
print(df_clean[['title', 'company_name', 'location', 'posted_at']].head())

print("\nSalary data completeness:")
print(f"Has salary: 0 (0.0%) - No salary data in this dataset")

# Save
print("\nSaving cleaned data...")
df_clean.to_csv('data/processed/linkedin_data_cleaned.csv', index=False)
print("Saved to data/processed/linkedin_data_cleaned.csv")

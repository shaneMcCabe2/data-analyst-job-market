import pandas as pd

print("Loading LinkedIn USA dataset...")
df = pd.read_csv('linkedin-data-analyst-jobs-listings/linkedin-jobs-usa.csv')
print(f"Original rows: {len(df):,}")

# 1. Basic cleaning
print("\nCleaning data...")
df_usa = df.copy()
df_usa['location'] = df_usa['location'].str.strip()
df_usa['company'] = df_usa['company'].str.strip()

# Show sample locations
print("\nSample locations:")
print(df_usa['location'].value_counts().head(10))

# 2. Parse onsite_remote field
print("\nWork type distribution:")
print(df_usa['onsite_remote'].value_counts())

# Map onsite_remote to our work_type
work_type_map = {
    'onsite': 'Onsite',
    'remote': 'Remote',
    'hybrid': 'Hybrid'
}
df_usa['work_type_clean'] = df_usa['onsite_remote'].map(work_type_map).fillna('Not Specified')

# 3. Map to unified schema
print("\nMapping to unified schema...")
df_clean = pd.DataFrame({
    'title': df_usa['title'],
    'company_name': df_usa['company'],
    'location': df_usa['location'],
    'description': df_usa['description'],
    'posted_at': df_usa['posted_date'],
    'salary_min': None,
    'salary_max': None,
    'work_type': df_usa['work_type_clean'],
    'source': 'LinkedIn USA 2022',
    'url': df_usa['link']
})

print(f"\nFinal cleaned rows: {len(df_clean):,}")

# Stats
print("\nSample of cleaned data:")
print(df_clean[['title', 'company_name', 'location', 'work_type', 'posted_at']].head())

print("\nWork type distribution:")
print(df_clean['work_type'].value_counts())

# Save
print("\nSaving cleaned data...")
df_clean.to_csv('data/processed/linkedin_usa_cleaned.csv', index=False)
print("Saved to data/processed/linkedin_usa_cleaned.csv")

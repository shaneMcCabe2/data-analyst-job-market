import pandas as pd

print("Loading Indeed 2024 data...")
df = pd.read_csv('indeed-biweekly-2024/all_vacancies.csv', low_memory=False)
print(f"Total rows: {len(df):,}")

# Filter for Data Analyst jobs (use .copy() to avoid warning)
print("\nFiltering for Data Analyst jobs...")
da_keywords = ['data analyst', 'business analyst', 'analytics']
pattern = '|'.join(da_keywords)
df_da = df[df['job_title'].str.contains(pattern, case=False, na=False)].copy()
print(f"Data Analyst jobs: {len(df_da):,}")

# Create date field
df_da['posted_date_clean'] = pd.to_datetime(
    '2024-' + df_da['scrape_month'].astype(str) + '-' + df_da['scrape_day'].astype(str),
    format='%Y-%m-%d',
    errors='coerce'
)

# Extract experience level from job title
def extract_experience_level(title):
    if pd.isna(title):
        return 'Not Specified'
    title_lower = title.lower()
    if any(word in title_lower for word in ['senior', 'sr.', 'sr ', 'lead', 'principal']):
        return 'Senior'
    elif any(word in title_lower for word in ['entry', 'junior', 'jr.', 'jr ', 'associate']):
        return 'Entry'
    elif any(word in title_lower for word in ['ii', ' 2', 'mid-level']):
        return 'Mid'
    else:
        return 'Mid'

df_da['experience_level'] = df_da['job_title'].apply(extract_experience_level)

# Map to unified schema
print("\nMapping to unified schema...")
df_clean = pd.DataFrame({
    'job_id': range(1, len(df_da) + 1),
    'title': df_da['job_title'],
    'company_name': df_da['company'],
    'location': df_da['location'],
    'description': df_da['text_full'],
    'posted_date_clean': df_da['posted_date_clean'],
    'salary_min': None,
    'salary_max': None,
    'work_type': 'Not Specified',
    'experience_level': df_da['experience_level'],
    'skills_text': '',
    'software_text': '',
    'source': 'Indeed 2024'
})

print(f"\nFinal cleaned rows: {len(df_clean):,}")
print("\nExperience level distribution:")
print(df_clean['experience_level'].value_counts())

# Save
print("\nSaving cleaned data...")
df_clean.to_csv('data/processed/indeed_2024_cleaned.csv', index=False)
print("Saved to data/processed/indeed_2024_cleaned.csv")

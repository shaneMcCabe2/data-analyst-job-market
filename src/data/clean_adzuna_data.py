import pandas as pd

print("Loading Adzuna raw data...")
df = pd.read_csv('data/processed/adzuna_raw.csv')
print(f"Total rows: {len(df):,}")

# Extract experience level from title
def extract_experience_level(title):
    if pd.isna(title):
        return 'Not Specified'
    title_lower = title.lower()
    if any(word in title_lower for word in ['senior', 'sr.', 'sr ', 'lead', 'principal', 'staff']):
        return 'Senior'
    elif any(word in title_lower for word in ['entry', 'junior', 'jr.', 'jr ', 'associate', 'graduate']):
        return 'Entry'
    elif any(word in title_lower for word in ['ii', ' 2', 'mid-level']):
        return 'Mid'
    else:
        return 'Mid'

df['experience_level'] = df['title'].apply(extract_experience_level)

# Parse location to get display name
df['location_clean'] = df['location'].apply(lambda x: x.get('display_name') if isinstance(x, dict) else x)
df['company_clean'] = df['company'].apply(lambda x: x.get('display_name') if isinstance(x, dict) else x)

# Convert created date to clean format
df['posted_date_clean'] = pd.to_datetime(df['created']).dt.strftime('%Y-%m-%d')

# Determine work type from contract_type
def get_work_type(contract_type, contract_time):
    if pd.isna(contract_type):
        return 'Not Specified'
    contract_type_lower = str(contract_type).lower()
    if 'remote' in contract_type_lower:
        return 'Remote'
    elif 'contract' in contract_type_lower:
        return 'Contract'
    return 'Not Specified'

df['work_type'] = df.apply(lambda row: get_work_type(row['contract_type'], row['contract_time']), axis=1)

# Map to unified schema
print("\nMapping to unified schema...")
df_clean = pd.DataFrame({
    'job_id': range(1, len(df) + 1),
    'title': df['title'],
    'company_name': df['company_clean'],
    'location': df['location_clean'],
    'description': df['description'],
    'posted_date_clean': df['posted_date_clean'],
    'salary_min': df['salary_min'],
    'salary_max': df['salary_max'],
    'work_type': df['work_type'],
    'experience_level': df['experience_level'],
    'skills_text': '',
    'software_text': '',
    'source': 'Adzuna Oct 2025'
})

print(f"\nFinal cleaned rows: {len(df_clean):,}")

# Stats
print("\nExperience level distribution:")
print(df_clean['experience_level'].value_counts())

print("\nWork type distribution:")
print(df_clean['work_type'].value_counts())

print("\nSalary data completeness:")
has_salary = df_clean['salary_min'].notna().sum()
print(f"Has salary: {has_salary:,} ({has_salary/len(df_clean)*100:.1f}%)")

print("\nDate distribution:")
print(df_clean['posted_date_clean'].value_counts().sort_index())

# Save
print("\nSaving cleaned data...")
df_clean.to_csv('data/processed/adzuna_cleaned.csv', index=False)
print("Saved to data/processed/adzuna_cleaned.csv")

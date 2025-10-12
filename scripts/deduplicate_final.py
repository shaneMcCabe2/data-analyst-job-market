"""
Deduplicate final combined dataset
"""

import pandas as pd
import re

print("Loading combined dataset...")
df = pd.read_csv('data/processed/jobs_all_combined.csv')
print(f"Total jobs: {len(df):,}")

# Normalization functions
def normalize_text(text):
    if pd.isna(text):
        return ""
    text = str(text).lower().strip()
    text = re.sub(r'\s+', ' ', text)
    return text

def normalize_company(company):
    text = normalize_text(company)
    # Remove common suffixes
    text = re.sub(r'\b(inc|llc|ltd|corporation|corp|co|company)\b\.?', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def normalize_title(title):
    text = normalize_text(title)
    # Remove level indicators
    text = re.sub(r'\b(i{1,3}|iv|v|vi|1|2|3|4)\b', '', text)
    text = re.sub(r'\b(entry|senior|jr|sr|junior|mid|level)\b', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

print("\nNormalizing fields...")
df['company_norm'] = df['company_name'].apply(normalize_company)
df['title_norm'] = df['title'].apply(normalize_title)
df['location_norm'] = df['location'].apply(normalize_text)

# Create composite key
df['composite_key'] = (
    df['company_norm'] + '|' + 
    df['title_norm'] + '|' + 
    df['location_norm']
)

print("\nFinding duplicates...")
# Mark duplicates (keep first occurrence)
df['is_duplicate'] = df.duplicated(subset=['composite_key'], keep='first')

duplicates = df['is_duplicate'].sum()
print(f"Found {duplicates:,} duplicate jobs")
print(f"Keeping {len(df) - duplicates:,} unique jobs")

# Show duplicate statistics by source
print("\nDuplicates by source:")
dup_by_source = df[df['is_duplicate']].groupby('source').size().sort_values(ascending=False)
print(dup_by_source)

# Remove duplicates
df_clean = df[~df['is_duplicate']].copy()

# Drop normalization columns
df_clean = df_clean.drop(columns=['company_norm', 'title_norm', 'location_norm', 
                                    'composite_key', 'is_duplicate'])

# Reset job_id
df_clean['job_id'] = range(1, len(df_clean) + 1)

print(f"\nFinal dataset: {len(df_clean):,} jobs")

# Save
df_clean.to_csv('data/processed/jobs_final_deduplicated.csv', index=False)
print("Saved to: data/processed/jobs_final_deduplicated.csv")

# Summary statistics
print("\n" + "="*60)
print("FINAL DATASET SUMMARY")
print("="*60)
print(f"\nTotal jobs: {len(df_clean):,}")
print(f"\nBy source:")
print(df_clean['source'].value_counts())
print(f"\nDate range:")
print(f"  {df_clean['posted_date_clean'].min()} to {df_clean['posted_date_clean'].max()}")
print(f"\nJobs with salary: {df_clean['salary_min'].notna().sum():,}")
print(f"\nBy experience level:")
print(df_clean['experience_level'].value_counts())

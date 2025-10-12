"""
Create final consolidated dataset for analysis
Combines: Adzuna, Google, LinkedIn, Indeed 2024, USAJobs
"""

import pandas as pd

print("Loading all data sources...")

# Load each source
df_adzuna = pd.read_csv('data/processed/adzuna_cleaned.csv')
df_google = pd.read_csv('data/processed/google_search_cleaned.csv')
df_linkedin = pd.read_csv('data/processed/linkedin_data_cleaned.csv')
df_linkedin_usa = pd.read_csv('data/processed/linkedin_usa_cleaned.csv')
df_indeed = pd.read_csv('data/processed/indeed_2024_cleaned.csv')
df_usajobs = pd.read_csv('data/processed/usajobs_analysts.csv')

print(f"Adzuna: {len(df_adzuna):,}")
print(f"Google: {len(df_google):,}")
print(f"LinkedIn: {len(df_linkedin):,}")
print(f"LinkedIn USA: {len(df_linkedin_usa):,}")
print(f"Indeed 2024: {len(df_indeed):,}")
print(f"USAJobs: {len(df_usajobs):,}")

# Combine all
df_all = pd.concat([
    df_adzuna,
    df_google,
    df_linkedin,
    df_linkedin_usa,
    df_indeed,
    df_usajobs
], ignore_index=True)

print(f"\nTotal before deduplication: {len(df_all):,}")

# Add unique ID
df_all['job_id'] = range(1, len(df_all) + 1)

# Save pre-deduplication
df_all.to_csv('data/processed/jobs_all_combined.csv', index=False)

print(f"\nSaved to: data/processed/jobs_all_combined.csv")
print("\nNext step: Run deduplication")

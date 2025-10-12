"""Collect all USAJobs data-related positions"""

import sys
sys.path.append('.')

from src.data.usajobs_collector import USAJobsCollector

collector = USAJobsCollector()

# Collect with "data" keyword (broader search)
raw_jobs = collector.search_jobs(
    keyword="data",  # Broader term
    results_per_page=500,
    max_pages=20
)

# Parse
df = collector.parse_jobs(raw_jobs)

# Filter for analyst positions in post-processing
print("\nFiltering for analyst-related positions...")
analyst_keywords = ['analyst', 'analytics', 'analysis', 'intelligence', 'business intelligence']
df_filtered = df[df['title'].str.contains('|'.join(analyst_keywords), case=False, na=False)]

print(f"After filtering: {len(df_filtered)} analyst jobs out of {len(df)} total")

# Save both
df.to_csv('data/processed/usajobs_all_data.csv', index=False)
df_filtered.to_csv('data/processed/usajobs_analysts.csv', index=False)

print("\nSaved:")
print("  - All data jobs: data/processed/usajobs_all_data.csv")
print("  - Filtered analysts: data/processed/usajobs_analysts.csv")

# Summary
print(f"\nFiltered dataset summary:")
print(f"Total: {len(df_filtered)}")
print(f"With salary: {df_filtered['salary_min'].notna().sum()}")
print(f"Date range: {df_filtered['posted_date_clean'].min()} to {df_filtered['posted_date_clean'].max()}")

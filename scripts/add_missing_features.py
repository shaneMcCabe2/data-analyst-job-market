"""
Add missing features to final dataset
Extracts experience level and state for all jobs
"""

import pandas as pd
import re

def extract_experience_level(title):
    if pd.isna(title):
        return 'Not Specified'
    
    title_lower = title.lower()
    
    # Check for Director/Executive FIRST
    if any(word in title_lower for word in ['director', 'executive', 'vp', 'vice president', 'chief']):
        return 'Senior'
    
    # Senior level
    if any(word in title_lower for word in ['senior', 'sr.', 'sr ', 'lead', 'principal', 'staff']):
        return 'Senior'
    
    # Entry level (but NOT "associate director")
    if 'associate' in title_lower and 'director' not in title_lower:
        return 'Entry'
    
    if any(word in title_lower for word in ['entry', 'junior', 'jr.', 'jr ', 'graduate']):
        return 'Entry'
    
    # Mid level
    if any(word in title_lower for word in ['ii', ' 2', 'mid-level']):
        return 'Mid'
    
    return 'Mid'

print("Loading final dataset...")
df = pd.read_csv('data/processed/jobs_final_deduplicated.csv')
print(f"Total jobs: {len(df):,}")

# Extract experience level for all jobs that don't have it
print("\nExtracting experience levels...")
df['experience_level'] = df.apply(
    lambda row: extract_experience_level(row['title']) if pd.isna(row['experience_level']) else row['experience_level'],
    axis=1
)

print("\nExperience level distribution:")
print(df['experience_level'].value_counts())

# Save updated dataset
df.to_csv('data/processed/jobs_final_complete.csv', index=False)
print(f"\nSaved to: data/processed/jobs_final_complete.csv")

# Summary
print("\n" + "="*60)
print("COMPLETE DATASET SUMMARY")
print("="*60)
print(f"Total jobs: {len(df):,}")
print(f"With salary: {df['salary_min'].notna().sum():,} ({df['salary_min'].notna().sum()/len(df)*100:.1f}%)")
print(f"\nBy experience level:")
print(df['experience_level'].value_counts())

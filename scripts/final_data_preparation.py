"""
Final data preparation - add all features needed for analysis
"""

import pandas as pd
import re
import ast
from datetime import datetime

print("Loading dataset...")
df = pd.read_csv('data/processed/jobs_final_complete.csv')
print(f"Total jobs: {len(df):,}")

# =========================================
# 1. PARSE ADZUNA DICTIONARY FIELDS
# =========================================
print("\n1. Parsing Adzuna dictionary fields...")

def parse_adzuna_field(field, key='display_name'):
    """Parse Adzuna dictionary strings"""
    if pd.isna(field):
        return None
    
    field_str = str(field)
    
    if '__CLASS__' in field_str and 'Adzuna' in field_str:
        try:
            field_dict = ast.literal_eval(field_str)
            return field_dict.get(key, None)
        except:
            return field_str
    
    return field_str

df['company_name'] = df['company_name'].apply(lambda x: parse_adzuna_field(x, 'display_name'))
df['location'] = df['location'].apply(lambda x: parse_adzuna_field(x, 'display_name'))

print("Adzuna fields parsed")

# =========================================
# 2. EXTRACT STATE
# =========================================
print("\n2. Extracting state from locations...")

US_STATES = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
    'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY',
    'District of Columbia': 'DC'
}

STATE_ABBREV = {abbrev: name for name, abbrev in US_STATES.items()}

def extract_state(location):
    if pd.isna(location):
        return None
    
    location_str = str(location)
    
    # Remote/Anywhere
    if any(word in location_str.lower() for word in ['remote', 'anywhere']):
        return 'Remote'
    
    # Pattern 1: "City, ST"
    match = re.search(r',\s*([A-Z]{2})(?:\s|$)', location_str)
    if match:
        abbrev = match.group(1)
        if abbrev in STATE_ABBREV:
            return abbrev
    
    # Pattern 2: Full state name
    for state_name, abbrev in US_STATES.items():
        if state_name in location_str:
            return abbrev
    
    # Unknown
    if 'united states' in location_str.lower():
        return 'Unknown'
    
    return 'Unknown'

df['state'] = df['location'].apply(extract_state)

print(f"States extracted. Remote: {(df['state'] == 'Remote').sum():,}, Unknown: {(df['state'] == 'Unknown').sum():,}")

# =========================================
# 3. ADD SALARY AVERAGE
# =========================================
print("\n3. Calculating salary average...")

df['salary_avg'] = (df['salary_min'] + df['salary_max']) / 2

print(f"Salary avg calculated for {df['salary_avg'].notna().sum():,} jobs")

# =========================================
# 4. ADD DATE FEATURES
# =========================================
print("\n4. Extracting date features...")

df['posted_date_clean'] = pd.to_datetime(df['posted_date_clean'], errors='coerce')
df['year'] = df['posted_date_clean'].dt.year
df['month'] = df['posted_date_clean'].dt.month
df['quarter'] = df['posted_date_clean'].dt.quarter

print(f"Date features extracted for {df['year'].notna().sum():,} jobs")

# =========================================
# 5. ADD DERIVED FEATURES
# =========================================
print("\n5. Adding derived features...")

# Remote flag
df['is_remote'] = df['work_type'].str.contains('Remote', case=False, na=False) | (df['state'] == 'Remote')

# Has salary flag
df['has_salary'] = df['salary_min'].notna()

# Skills count (if skills_text exists and is not empty)
df['skills_count'] = df['skills_text'].apply(lambda x: len(str(x).split(',')) if pd.notna(x) and str(x).strip() != '' else 0)

# Software count
df['software_count'] = df['software_text'].apply(lambda x: len(str(x).split(',')) if pd.notna(x) and str(x).strip() != '' else 0)

print("Derived features added")

# =========================================
# 6. FINAL CLEANUP
# =========================================
print("\n6. Final cleanup...")

# Drop unnecessary columns
cols_to_drop = ['posted_at']
df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])

# Reorder columns logically
cols_order = [
    'job_id', 'title', 'company_name', 'location', 'state',
    'posted_date_clean', 'year', 'month', 'quarter',
    'salary_min', 'salary_max', 'salary_avg', 'has_salary',
    'experience_level', 'work_type', 'is_remote',
    'skills_text', 'skills_count', 'software_text', 'software_count',
    'description', 'source', 'url'
]

# Only reorder columns that exist
cols_order = [col for col in cols_order if col in df.columns]
df = df[cols_order]

# =========================================
# 7. SAVE FINAL DATASET
# =========================================
print("\n7. Saving final analysis-ready dataset...")

output_file = 'data/processed/jobs_analysis_ready.csv'
df.to_csv(output_file, index=False)

print(f"Saved to: {output_file}")

# =========================================
# 8. FINAL SUMMARY
# =========================================
print("\n" + "="*60)
print("ANALYSIS-READY DATASET")
print("="*60)
print(f"Total jobs: {len(df):,}")
print(f"\nSalary data: {df['has_salary'].sum():,} ({df['has_salary'].sum()/len(df)*100:.1f}%)")
print(f"Remote jobs: {df['is_remote'].sum():,} ({df['is_remote'].sum()/len(df)*100:.1f}%)")
print(f"\nDate range: {df['year'].min():.0f}-{df['year'].max():.0f}")
print(f"  2024: {(df['year'] == 2024).sum():,}")
print(f"  2025: {(df['year'] == 2025).sum():,}")
print(f"\nTop 10 states:")
print(df['state'].value_counts().head(10))
print(f"\nExperience levels:")
print(df['experience_level'].value_counts())
print(f"\nColumns: {len(df.columns)}")
print(df.columns.tolist())

print("\n" + "="*60)
print("DATA PREPARATION COMPLETE - READY FOR ANALYSIS")
print("="*60)

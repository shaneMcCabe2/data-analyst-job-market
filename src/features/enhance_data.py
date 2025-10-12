import pandas as pd
import re
from datetime import datetime, timedelta

print("Loading jobs data...")
df = pd.read_csv('data/processed/jobs_combined.csv')
print(f"Loaded {len(df):,} rows")

# =========================================
# STEP 1: EXTRACT EXPERIENCE LEVEL
# =========================================
print("\n" + "="*50)
print("STEP 1: Extracting Experience Level")
print("="*50)

def extract_experience_level(title):
    """Extract experience level from job title"""
    if pd.isna(title):
        return 'Not Specified'
    
    title_lower = title.lower()
    
    # Senior level keywords
    if any(word in title_lower for word in ['senior', 'sr.', 'sr ', 'lead', 'principal', 'staff', 'architect']):
        return 'Senior'
    
    # Entry level keywords
    elif any(word in title_lower for word in ['entry', 'junior', 'jr.', 'jr ', 'associate', 'entry-level', 'recent graduate', 'graduate']):
        return 'Entry'
    
    # Mid level (including numbered levels like "II", "2")
    elif any(word in title_lower for word in ['ii', ' 2', 'mid-level', 'intermediate']):
        return 'Mid'
    
    # Default to Mid if no clear indicator
    else:
        return 'Mid'

df['experience_level'] = df['title'].apply(extract_experience_level)

print("\nExperience level distribution:")
print(df['experience_level'].value_counts())

# =========================================
# STEP 2: EXTRACT SKILLS AND SOFTWARE
# =========================================
print("\n" + "="*50)
print("STEP 2: Extracting Skills and Software")
print("="*50)

# Define comprehensive skills and software lists
SKILLS = [
    'python', 'sql', 'r programming', 'java', 'scala', 'javascript',
    'statistics', 'machine learning', 'data analysis', 'data modeling',
    'etl', 'data warehousing', 'data mining', 'predictive modeling',
    'a/b testing', 'statistical analysis', 'regression', 'forecasting',
    'data visualization', 'dashboard', 'reporting', 'kpi', 'metrics'
]

SOFTWARE = [
    'excel', 'tableau', 'power bi', 'powerbi', 'looker', 'qlik',
    'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch',
    'spark', 'hadoop', 'kafka', 'airflow',
    'aws', 'azure', 'gcp', 'snowflake', 'redshift', 'bigquery',
    'postgresql', 'mysql', 'mongodb', 'oracle', 'sql server',
    'jupyter', 'git', 'docker', 'kubernetes',
    'sas', 'spss', 'stata', 'matlab'
]

def extract_skills(description):
    """Extract skills from job description"""
    if pd.isna(description):
        return []
    
    desc_lower = description.lower()
    found_skills = []
    
    for skill in SKILLS:
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, desc_lower):
            found_skills.append(skill.title())
    
    return found_skills

def extract_software(description):
    """Extract software from job description"""
    if pd.isna(description):
        return []
    
    desc_lower = description.lower()
    found_software = []
    
    for software in SOFTWARE:
        pattern = r'\b' + re.escape(software) + r'\b'
        if re.search(pattern, desc_lower):
            found_software.append(software.title())
    
    return found_software

print("Extracting skills and software (this may take a minute)...")
df['skills'] = df['description'].apply(extract_skills)
df['software'] = df['description'].apply(extract_software)

# Convert lists to comma-separated strings for easier use in Tableau
df['skills_text'] = df['skills'].apply(lambda x: ', '.join(x) if x else '')
df['software_text'] = df['software'].apply(lambda x: ', '.join(x) if x else '')

print("\nTop 10 most mentioned skills:")
all_skills = [skill for skills_list in df['skills'] for skill in skills_list]
skills_counts = pd.Series(all_skills).value_counts().head(10)
print(skills_counts)

print("\nTop 10 most mentioned software:")
all_software = [sw for software_list in df['software'] for sw in software_list]
software_counts = pd.Series(all_software).value_counts().head(10)
print(software_counts)

# =========================================
# STEP 3: STANDARDIZE DATES
# =========================================
print("\n" + "="*50)
print("STEP 3: Standardizing Dates")
print("="*50)

def parse_posted_date(posted_str, source):
    """Convert various date formats to standard YYYY-MM-DD"""
    if pd.isna(posted_str):
        return None
    
    posted_str = str(posted_str).strip()
    
    # If already in YYYY-MM-DD format (LinkedIn data)
    if re.match(r'\d{4}-\d{2}-\d{2}', posted_str):
        return posted_str
    
    # Handle relative dates like "15 hours ago", "2 days ago"
    # Assume data was collected around April 2025 for Google Search
    reference_date = datetime(2025, 4, 18)  # Google search data collection date
    
    if 'hour' in posted_str.lower():
        hours = int(re.search(r'(\d+)', posted_str).group(1))
        date = reference_date - timedelta(hours=hours)
        return date.strftime('%Y-%m-%d')
    
    elif 'day' in posted_str.lower():
        days = int(re.search(r'(\d+)', posted_str).group(1))
        date = reference_date - timedelta(days=days)
        return date.strftime('%Y-%m-%d')
    
    elif 'week' in posted_str.lower():
        weeks = int(re.search(r'(\d+)', posted_str).group(1))
        date = reference_date - timedelta(weeks=weeks)
        return date.strftime('%Y-%m-%d')
    
    elif 'month' in posted_str.lower():
        months = int(re.search(r'(\d+)', posted_str).group(1))
        date = reference_date - timedelta(days=months*30)
        return date.strftime('%Y-%m-%d')
    
    elif 'today' in posted_str.lower():
        return reference_date.strftime('%Y-%m-%d')
    
    elif 'yesterday' in posted_str.lower():
        date = reference_date - timedelta(days=1)
        return date.strftime('%Y-%m-%d')
    
    # If we can't parse it, return None
    return None

df['posted_date_clean'] = df.apply(lambda row: parse_posted_date(row['posted_at'], row['source']), axis=1)

print("\nDate parsing results:")
print(f"Successfully parsed: {df['posted_date_clean'].notna().sum():,} ({df['posted_date_clean'].notna().sum()/len(df)*100:.1f}%)")
print(f"Failed to parse: {df['posted_date_clean'].isna().sum():,}")

# Show date range (skip NaN values)
valid_dates = df['posted_date_clean'].dropna()
print(f"\nDate range: {valid_dates.min()} to {valid_dates.max()}")

# =========================================
# SAVE ENHANCED DATASET
# =========================================
print("\n" + "="*50)
print("SAVING ENHANCED DATASET")
print("="*50)

# Save full enhanced dataset
df.to_csv('data/processed/jobs_enhanced.csv', index=False)
print("Saved to data/processed/jobs_enhanced.csv")

# Create Tableau-ready version
df_tableau = df[[
    'job_id', 'title', 'company_name', 'location', 
    'posted_date_clean', 'salary_min', 'salary_max', 
    'work_type', 'experience_level', 
    'skills_text', 'software_text', 'source'
]].copy()

df_tableau.to_csv('data/tableau/jobs_enhanced_tableau.csv', index=False)
print("Saved to data/tableau/jobs_enhanced_tableau.csv")

print("\nENHANCEMENT COMPLETE")

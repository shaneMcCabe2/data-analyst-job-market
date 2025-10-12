"""
Skills Extraction Script
Parses job descriptions to identify technical skills and tools
"""

import pandas as pd
import re
from collections import Counter

# Configuration
INPUT_FILE = 'data/processed/jobs_analysis_ready.csv'
OUTPUT_FILE = 'data/processed/jobs_with_skills.csv'

# Comprehensive skills dictionary
SKILLS_DATABASE = {
    # Programming Languages
    'python': ['python', 'py'],
    'r': [r'\br\b', r'\br lang', 'r programming', 'r studio', 'rstudio'],
    'sql': ['sql', 'mysql', 'postgresql', 'postgres', 't-sql', 'tsql', 'pl/sql', 'plsql'],
    'sas': ['sas'],
    'java': ['java'],
    'scala': ['scala'],
    'javascript': ['javascript', 'js'],
    
    # BI & Visualization Tools
    'tableau': ['tableau'],
    'power bi': ['power bi', 'powerbi', 'power-bi'],
    'looker': ['looker'],
    'qlik': ['qlik', 'qlikview', 'qlik sense'],
    'excel': ['excel', 'microsoft excel', 'ms excel', 'advanced excel'],
    'google sheets': ['google sheets', 'gsheets'],
    
    # Databases
    'mongodb': ['mongodb', 'mongo'],
    'oracle': ['oracle', 'oracle db'],
    'snowflake': ['snowflake'],
    'redshift': ['redshift', 'amazon redshift'],
    'bigquery': ['bigquery', 'big query', 'google bigquery'],
    'mysql': ['mysql'],
    'postgresql': ['postgresql', 'postgres'],
    'sql server': ['sql server', 'mssql', 'ms sql'],
    
    # Cloud Platforms
    'aws': ['aws', 'amazon web services'],
    'azure': ['azure', 'microsoft azure'],
    'gcp': ['gcp', 'google cloud', 'google cloud platform'],
    
    # Data Tools & Frameworks
    'spark': ['spark', 'apache spark', 'pyspark'],
    'hadoop': ['hadoop'],
    'airflow': ['airflow', 'apache airflow'],
    'kafka': ['kafka', 'apache kafka'],
    'dbt': ['dbt', 'data build tool'],
    'pandas': ['pandas'],
    'numpy': ['numpy'],
    
    # Statistics & ML
    'statistics': ['statistics', 'statistical analysis', 'statistical modeling'],
    'machine learning': ['machine learning', 'ml', 'predictive modeling'],
    'regression': ['regression', 'linear regression', 'logistic regression'],
    'a/b testing': ['a/b test', 'ab test', 'a-b test', 'split test'],
    
    # Other Skills
    'git': ['git', 'github', 'gitlab', 'version control'],
    'api': ['api', 'rest api', 'restful'],
    'etl': ['etl', 'data pipeline'],
    'data modeling': ['data modeling', 'data model'],
    'data warehouse': ['data warehouse', 'data warehousing', 'dwh'],
    'data visualization': ['data visualization', 'data viz'],
    'business intelligence': ['business intelligence', 'bi'],
    'agile': ['agile', 'scrum'],
}


def clean_text(text):
    """Convert text to lowercase and handle None values"""
    if pd.isna(text):
        return ''
    return str(text).lower()


def extract_skills(description):
    """
    Extract skills from job description
    Returns: list of matched skills
    """
    if pd.isna(description):
        return []
    
    text = clean_text(description)
    found_skills = []
    
    for skill_name, patterns in SKILLS_DATABASE.items():
        for pattern in patterns:
            # Use word boundaries for better matching
            regex_pattern = pattern if r'\b' in pattern else r'\b' + re.escape(pattern) + r'\b'
            if re.search(regex_pattern, text):
                found_skills.append(skill_name)
                break  # Only add skill once
    
    return found_skills


def process_jobs(input_file):
    """Load data and extract skills from all job descriptions"""
    
    print(f"Loading data from {input_file}...")
    df = pd.read_csv(input_file, low_memory=False)
    print(f"Loaded {len(df):,} jobs")
    
    # Check if description column exists
    if 'description' not in df.columns:
        print("[ERROR] No 'description' column found in data")
        return None
    
    # Count non-null descriptions
    has_desc = df['description'].notna().sum()
    print(f"Jobs with descriptions: {has_desc:,} ({has_desc/len(df)*100:.1f}%)")
    
    if has_desc == 0:
        print("[ERROR] No job descriptions available to parse")
        return None
    
    # Extract skills
    print("\nExtracting skills from job descriptions...")
    print("This may take a few minutes for large datasets...")
    
    df['skills_extracted'] = df['description'].apply(extract_skills)
    df['skills_extracted_text'] = df['skills_extracted'].apply(lambda x: ', '.join(x) if x else '')
    df['skills_extracted_count'] = df['skills_extracted'].apply(len)
    
    # Stats
    jobs_with_skills = (df['skills_extracted_count'] > 0).sum()
    avg_skills = df['skills_extracted_count'].mean()
    
    print(f"\n[OK] Extraction complete!")
    print(f"Jobs with at least 1 skill: {jobs_with_skills:,} ({jobs_with_skills/len(df)*100:.1f}%)")
    print(f"Average skills per job: {avg_skills:.1f}")
    
    return df


def analyze_skill_frequency(df):
    """Analyze and display most common skills"""
    
    print("\n" + "="*70)
    print("SKILL FREQUENCY ANALYSIS")
    print("="*70)
    
    # Flatten all skills into a single list
    all_skills = []
    for skills_list in df['skills_extracted']:
        if isinstance(skills_list, list):
            all_skills.extend(skills_list)
    
    # Count frequencies
    skill_counts = Counter(all_skills)
    
    print(f"\nTotal unique skills identified: {len(skill_counts)}")
    print(f"Total skill mentions: {len(all_skills):,}")
    
    print("\nTop 20 Most In-Demand Skills:")
    print("-" * 70)
    
    for i, (skill, count) in enumerate(skill_counts.most_common(20), 1):
        percentage = (count / len(df)) * 100
        print(f"{i:2}. {skill:20} | {count:5,} jobs ({percentage:5.1f}%)")
    
    return skill_counts


def save_results(df, output_file):
    """Save processed data with extracted skills"""
    
    # Drop the list column (can't save lists to CSV easily)
    df_to_save = df.drop(columns=['skills_extracted'])
    
    df_to_save.to_csv(output_file, index=False)
    print(f"\n[OK] Saved results to {output_file}")
    
    # Also save summary statistics
    summary_file = output_file.replace('.csv', '_summary.csv')
    
    # Create summary DataFrame
    all_skills = []
    for skills_list in df['skills_extracted']:
        if isinstance(skills_list, list):
            all_skills.extend(skills_list)
    
    skill_counts = Counter(all_skills)
    
    summary_df = pd.DataFrame([
        {'skill': skill, 'job_count': count, 'percentage': (count/len(df))*100}
        for skill, count in skill_counts.most_common()
    ])
    
    summary_df.to_csv(summary_file, index=False)
    print(f"[OK] Saved skill summary to {summary_file}")


def main():
    """Main execution"""
    
    print("="*70)
    print("DATA ANALYST JOB MARKET: SKILLS EXTRACTION")
    print("="*70 + "\n")
    
    # Process jobs
    df = process_jobs(INPUT_FILE)
    
    if df is None:
        return
    
    # Analyze frequency
    analyze_skill_frequency(df)
    
    # Save results
    save_results(df, OUTPUT_FILE)
    
    print("\n" + "="*70)
    print("Next steps:")
    print("1. Use jobs_with_skills.csv for further analysis")
    print("2. Create visualizations of top skills")
    print("3. Analyze skill combinations and correlations")
    print("="*70)


if __name__ == '__main__':
    main()

"""
Work Type Classification Investigation
Check if remote classification is accurate
"""

import pandas as pd
import re

INPUT_FILE = 'data/processed/jobs_with_work_type.csv'


def investigate_remote_classification(df):
    """Check why so many jobs are classified as remote"""
    
    print("="*70)
    print("INVESTIGATION: REMOTE CLASSIFICATION")
    print("="*70 + "\n")
    
    # 1. Check by source
    print("WORK TYPE DISTRIBUTION BY SOURCE:")
    print("-"*70)
    source_work = pd.crosstab(df['source'], df['work_type'], margins=True)
    print(source_work)
    print()
    
    # 2. Sample remote job descriptions
    print("\nSAMPLE 'REMOTE' JOB DESCRIPTIONS (first 200 chars):")
    print("-"*70)
    
    remote_jobs = df[df['work_type'] == 'Remote'].copy()
    
    for i, row in remote_jobs.head(10).iterrows():
        title = row.get('title', 'N/A')
        desc = str(row.get('description', ''))[:200]
        source = row.get('source', 'N/A')
        
        print(f"\n{i+1}. {title} (Source: {source})")
        print(f"   {desc}...")
        
        # Check what triggered remote
        desc_lower = desc.lower()
        if 'remote' in desc_lower:
            print("   [Contains 'remote']")
        if 'work from home' in desc_lower or 'wfh' in desc_lower:
            print("   [Contains work from home/wfh]")
    
    print("\n" + "="*70)
    
    # 3. Check for false positives
    print("\nPOTENTIAL FALSE POSITIVES CHECK:")
    print("-"*70)
    
    # Look for jobs marked remote that might actually be onsite
    remote_with_location = remote_jobs[
        remote_jobs['description'].str.contains(
            r'(must be located|based in|office in|headquarters|commute)', 
            case=False, 
            na=False,
            regex=True
        )
    ]
    
    print(f"Remote jobs mentioning specific locations: {len(remote_with_location):,}")
    
    if len(remote_with_location) > 0:
        print("\nExamples:")
        for i, row in remote_with_location.head(5).iterrows():
            title = row.get('title', 'N/A')
            location = row.get('location', 'N/A')
            print(f"  - {title} | Location: {location}")
    
    print()
    
    # 4. Year trends
    if 'year' in df.columns:
        print("\nWORK TYPE BY YEAR:")
        print("-"*70)
        year_work = pd.crosstab(df['year'], df['work_type'], normalize='index') * 100
        year_work = year_work.round(1)
        print(year_work)
        print()


def check_keyword_frequency(df):
    """See how often remote keywords appear"""
    
    print("\nKEYWORD FREQUENCY IN DESCRIPTIONS:")
    print("-"*70)
    
    remote_jobs = df[df['work_type'] == 'Remote']
    
    keywords = {
        'remote': r'\bremote\b',
        'work from home': r'\bwork from home\b',
        'wfh': r'\bwfh\b',
        'telecommute': r'\btelecommute\b',
        'virtual': r'\bvirtual\b'
    }
    
    for keyword, pattern in keywords.items():
        count = remote_jobs['description'].str.contains(pattern, case=False, na=False, regex=True).sum()
        pct = (count / len(remote_jobs) * 100)
        print(f"{keyword:20} | {count:6,} jobs ({pct:5.1f}%)")
    
    print()


def suggest_reclassification(df):
    """Suggest jobs that might need reclassification"""
    
    print("\nSUGGESTED RECLASSIFICATION:")
    print("-"*70)
    
    remote_jobs = df[df['work_type'] == 'Remote'].copy()
    
    # Jobs that say "not remote" or "no remote work"
    not_remote = remote_jobs[
        remote_jobs['description'].str.contains(
            r'(not remote|no remote|isn\'t remote|not a remote|this is not a remote)',
            case=False,
            na=False,
            regex=True
        )
    ]
    
    print(f"Jobs marked Remote but description says 'not remote': {len(not_remote)}")
    
    # Jobs marked remote but have strong onsite indicators
    onsite_indicators = remote_jobs[
        remote_jobs['description'].str.contains(
            r'(in-person|on-site only|must work onsite|required to be in office)',
            case=False,
            na=False,
            regex=True
        )
    ]
    
    print(f"Jobs marked Remote with strong onsite indicators: {len(onsite_indicators)}")
    
    if len(not_remote) > 0 or len(onsite_indicators) > 0:
        print("\nRecommendation: Refine extraction logic to catch these edge cases")
    
    print()


def main():
    """Run investigation"""
    
    print("Loading data...")
    df = pd.read_csv(INPUT_FILE, low_memory=False)
    df = df[df['work_type'] != 'Not Specified'].copy()
    
    print(f"Loaded {len(df):,} jobs with specified work types\n")
    
    investigate_remote_classification(df)
    check_keyword_frequency(df)
    suggest_reclassification(df)
    
    print("="*70)
    print("CONCLUSION:")
    print("Check the samples above to see if classification seems reasonable.")
    print("If not, we can refine the extraction logic.")
    print("="*70)


if __name__ == '__main__':
    main()

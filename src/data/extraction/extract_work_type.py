"""
Work Type Extraction Script
Re-parses job descriptions to identify remote/hybrid/onsite
"""

import pandas as pd
import re

INPUT_FILE = 'data/processed/jobs_with_skills.csv'
OUTPUT_FILE = 'data/processed/jobs_with_work_type.csv'


def extract_work_type(description, title, existing_work_type):
    """
    Extract work type from job description and title
    Priority: existing_work_type > description keywords > default
    """
    
    # If already labeled (not "Not Specified"), keep it unless it's "Contract"
    if pd.notna(existing_work_type) and existing_work_type not in ['Not Specified', 'Contract', '']:
        return existing_work_type
    
    # Combine description and title for searching
    text = ''
    if pd.notna(description):
        text += str(description).lower()
    if pd.notna(title):
        text += ' ' + str(title).lower()
    
    if not text:
        return 'Not Specified'
    
    # Remote keywords (most specific first)
    remote_keywords = [
        r'\bremote\b', r'\bwork from home\b', r'\bwfh\b', r'\btelecommute\b',
        r'\bremote position\b', r'\bfully remote\b', r'\b100% remote\b',
        r'\bremote work\b', r'\bwork remotely\b', r'\bvirtual position\b'
    ]
    
    # Hybrid keywords
    hybrid_keywords = [
        r'\bhybrid\b', r'\bflexible schedule\b', r'\bflexible work\b',
        r'\bpartially remote\b', r'\bremote/office\b', r'\boffice/remote\b',
        r'\bsome remote\b', r'\bremote option\b'
    ]
    
    # Onsite keywords
    onsite_keywords = [
        r'\bon-site\b', r'\bonsite\b', r'\bin-office\b', r'\bin office\b',
        r'\bat office\b', r'\boffice based\b', r'\bin-person\b', r'\bin person\b'
    ]
    
    # Check for remote (highest priority for remote jobs)
    for pattern in remote_keywords:
        if re.search(pattern, text):
            # Make sure it's not "not remote" or "no remote"
            if not re.search(r'(not|no|isn\'t|isnt)\s+(remote|work from home)', text):
                return 'Remote'
    
    # Check for hybrid
    for pattern in hybrid_keywords:
        if re.search(pattern, text):
            return 'Hybrid'
    
    # Check for onsite
    for pattern in onsite_keywords:
        if re.search(pattern, text):
            return 'Onsite'
    
    # Default: if we can't determine, mark as Not Specified
    return 'Not Specified'


def process_work_types(input_file):
    """Process all jobs and extract work types"""
    
    print(f"Loading data from {input_file}...")
    df = pd.read_csv(input_file, low_memory=False)
    print(f"Loaded {len(df):,} jobs\n")
    
    # Show current distribution
    print("CURRENT WORK TYPE DISTRIBUTION:")
    print(df['work_type'].value_counts(dropna=False))
    print()
    
    # Extract work types
    print("Re-extracting work types from descriptions...")
    df['work_type_new'] = df.apply(
        lambda row: extract_work_type(
            row.get('description'), 
            row.get('title'),
            row.get('work_type')
        ), 
        axis=1
    )
    
    # Show new distribution
    print("\nNEW WORK TYPE DISTRIBUTION:")
    print(df['work_type_new'].value_counts())
    
    # Compare changes
    changed = (df['work_type'] != df['work_type_new']).sum()
    print(f"\nChanged: {changed:,} jobs ({changed/len(df)*100:.1f}%)")
    
    # Replace old column
    df['work_type'] = df['work_type_new']
    df = df.drop(columns=['work_type_new'])
    
    return df


def main():
    """Run extraction"""
    
    print("="*70)
    print("WORK TYPE EXTRACTION")
    print("="*70 + "\n")
    
    df = process_work_types(INPUT_FILE)
    
    # Save results
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n[OK] Saved to {OUTPUT_FILE}")
    
    print("\n" + "="*70)
    print("Run analyze_work_type.py again with the new file")
    print("="*70)


if __name__ == '__main__':
    main()

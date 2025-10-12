"""
Improved Work Type Extraction
Stricter rules to reduce false positives
"""

import pandas as pd
import re

INPUT_FILE = 'data/processed/jobs_with_skills.csv'
OUTPUT_FILE = 'data/processed/jobs_with_work_type_v2.csv'


def extract_work_type_improved(description, title, location):
    """
    Improved work type extraction with stricter rules
    """
    
    # Combine text for searching
    text = ''
    if pd.notna(description):
        text += str(description).lower()
    if pd.notna(title):
        text += ' ' + str(title).lower()
    
    if not text:
        return 'Not Specified'
    
    # NEGATIVE FILTERS - Check these first
    # If description explicitly says "not remote", mark as onsite
    not_remote_patterns = [
        r'not remote', r'no remote', r'isn\'t remote', r'isnt remote',
        r'not a remote', r'this is not a remote', r'no remote work'
    ]
    for pattern in not_remote_patterns:
        if re.search(pattern, text):
            return 'Onsite'
    
    # Strong onsite indicators
    strong_onsite = [
        r'must work onsite', r'required to be in office', r'in-person only',
        r'onsite only', r'on-site only', r'no remote option'
    ]
    for pattern in strong_onsite:
        if re.search(pattern, text):
            return 'Onsite'
    
    # HYBRID DETECTION - Check before remote
    # Hybrid keywords or patterns like "3 days office, 2 days remote"
    hybrid_patterns = [
        r'\bhybrid\b',
        r'[0-9]\s*days?\s*(in\s*)?(office|onsite|on-site)',  # "3 days office"
        r'[0-9]\s*days?\s*remote',  # "2 days remote" 
        r'partially remote',
        r'flexible work',
        r'remote/office',
        r'office/remote',
        r'some remote',
        r'option to work remote'
    ]
    
    for pattern in hybrid_patterns:
        if re.search(pattern, text):
            return 'Hybrid'
    
    # REMOTE DETECTION - Must be clearly fully remote
    # Look for strong remote indicators
    fully_remote_patterns = [
        r'fully remote', r'100% remote', r'completely remote',
        r'entirely remote', r'all remote', r'full remote',
        r'remote position', r'remote role', r'remote opportunity',
        r'work from home position', r'wfh position'
    ]
    
    for pattern in fully_remote_patterns:
        if re.search(pattern, text):
            return 'Remote'
    
    # Check title for remote (often reliable)
    if pd.notna(title):
        title_lower = str(title).lower()
        if re.search(r'\(remote\)|\[remote\]|remote -|- remote', title_lower):
            # But verify no office requirement
            if not re.search(r'office|onsite|on-site|in-person', text):
                return 'Remote'
    
    # General remote keyword - but only if no location specificity
    if re.search(r'\bremote\b', text):
        # Check for location requirements that suggest not fully remote
        location_requirements = [
            r'must be (located|based) (in|near)',
            r'located in.*required',
            r'based in.*required',
            r'must live (in|within)',
            r'commute to',
            r'office.*required',
            r'visit.*office',
            r'headquarters'
        ]
        
        has_location_req = any(re.search(pattern, text) for pattern in location_requirements)
        
        if has_location_req:
            return 'Hybrid'
        else:
            return 'Remote'
    
    # ONSITE DETECTION - Default if we see onsite keywords
    onsite_patterns = [
        r'\bonsite\b', r'\bon-site\b', r'\bin-office\b',
        r'\bin office\b', r'\boffice based\b', r'\bin-person\b'
    ]
    
    for pattern in onsite_patterns:
        if re.search(pattern, text):
            return 'Onsite'
    
    # DEFAULT - Can't determine
    return 'Not Specified'


def process_improved(input_file):
    """Process with improved extraction"""
    
    print(f"Loading data from {input_file}...")
    df = pd.read_csv(input_file, low_memory=False)
    print(f"Loaded {len(df):,} jobs\n")
    
    print("Extracting work types with improved logic...")
    df['work_type_v2'] = df.apply(
        lambda row: extract_work_type_improved(
            row.get('description'),
            row.get('title'),
            row.get('location')
        ),
        axis=1
    )
    
    # Compare old vs new
    print("\nCOMPARISON:")
    print("="*70)
    
    if 'work_type' in df.columns:
        print("\nOLD DISTRIBUTION:")
        print(df['work_type'].value_counts())
    
    print("\nNEW DISTRIBUTION (IMPROVED):")
    print(df['work_type_v2'].value_counts())
    
    # Show what changed
    if 'work_type' in df.columns:
        changed = df[df['work_type'] != df['work_type_v2']]
        print(f"\nChanged: {len(changed):,} jobs ({len(changed)/len(df)*100:.1f}%)")
        
        print("\nMajor reclassifications:")
        transitions = changed.groupby(['work_type', 'work_type_v2']).size().sort_values(ascending=False)
        print(transitions.head(10))
    
    # Replace column
    df['work_type'] = df['work_type_v2']
    df = df.drop(columns=['work_type_v2'])
    
    return df


def validate_results(df):
    """Quick validation of results"""
    
    print("\n" + "="*70)
    print("VALIDATION")
    print("="*70)
    
    # Check remote jobs
    remote = df[df['work_type'] == 'Remote']
    
    # How many actually contain "remote"?
    has_remote_keyword = remote['description'].str.contains(r'\bremote\b', case=False, na=False, regex=True).sum()
    pct = (has_remote_keyword / len(remote) * 100) if len(remote) > 0 else 0
    
    print(f"\nRemote jobs containing 'remote' keyword: {has_remote_keyword:,} / {len(remote):,} ({pct:.1f}%)")
    
    # Check for location requirements
    has_location = remote['description'].str.contains(
        r'(must be located|based in.*required|must live in)',
        case=False, na=False, regex=True
    ).sum()
    
    print(f"Remote jobs with location requirements: {has_location:,} ({has_location/len(remote)*100:.1f}%)")
    
    print("\nImprovement: Remote classification should be more accurate now.")


def main():
    """Run improved extraction"""
    
    print("="*70)
    print("IMPROVED WORK TYPE EXTRACTION")
    print("="*70 + "\n")
    
    df = process_improved(INPUT_FILE)
    validate_results(df)
    
    # Save
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n[OK] Saved to {OUTPUT_FILE}")
    
    print("\n" + "="*70)
    print("Update analyze_work_type.py to use:")
    print("INPUT_FILE = 'data/processed/jobs_with_work_type_v2.csv'")
    print("="*70)


if __name__ == '__main__':
    main()

"""
Filter dataset to 2025 sources only
Removes old data from 2022, 2024
"""

import pandas as pd

INPUT_FILE = 'data/processed/jobs_with_work_type_v2.csv'
OUTPUT_FILE = 'data/processed/jobs_2025_only.csv'


def filter_to_2025(input_file):
    """Keep only 2025 data"""
    
    print("Loading data...")
    df = pd.read_csv(input_file, low_memory=False)
    print(f"Total jobs: {len(df):,}\n")
    
    # Show current sources
    print("CURRENT SOURCES:")
    print(df['source'].value_counts())
    print()
    
    # Sources to remove (pre-2025 or low quality)
    sources_to_remove = ['Indeed 2024', 'LinkedIn USA 2022', 'USAJobs']
    
    # Keep: Google Search (April 2025), Adzuna Oct 2025, LinkedIn (recent)
    print(f"Removing sources: {sources_to_remove}")
    df = df[~df['source'].isin(sources_to_remove)].copy()
    
    print(f"\nRemaining jobs: {len(df):,}")
    print("\nREMAINING SOURCES:")
    print(df['source'].value_counts())
    
    return df


def main():
    """Run filter"""
    
    print("="*70)
    print("FILTER TO 2025 DATA ONLY")
    print("="*70 + "\n")
    
    df = filter_to_2025(INPUT_FILE)
    
    # Save
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n[OK] Saved to {OUTPUT_FILE}")
    print(f"\nNext: Add RapidAPI data source")


if __name__ == '__main__':
    main()

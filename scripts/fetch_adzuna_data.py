import requests
import pandas as pd
import time
from datetime import datetime

APP_ID = "14fa5f1a"
APP_KEY = "325b34ce9bd68c10211365b942e18f8b"
BASE_URL = "https://api.adzuna.com/v1/api/jobs/us/search"

def fetch_adzuna_jobs():
    """Fetch all data analyst jobs from Adzuna"""
    
    all_jobs = []
    page = 1
    results_per_page = 50  # Max results per page
    total_fetched = 0
    
    print("Starting Adzuna data collection...")
    print(f"Target: ~17,737 jobs from last 120 days")
    print("="*50)
    
    while True:
        # Build URL with page number
        url = f"{BASE_URL}/{page}"
        
        params = {
            'app_id': APP_ID,
            'app_key': APP_KEY,
            'what': 'data analyst',
            'results_per_page': results_per_page,
            'max_days_old': 120,  # Get last 4 months
            'sort_by': 'date'
        }
        
        print(f"\nFetching page {page}...", end=" ")
        
        try:
            response = requests.get(url, params=params)
            
            if response.status_code != 200:
                print(f"Error {response.status_code}")
                break
            
            data = response.json()
            results = data.get('results', [])
            
            if not results:
                print("No more results")
                break
            
            all_jobs.extend(results)
            total_fetched += len(results)
            
            print(f"Got {len(results)} jobs. Total: {total_fetched:,}")
            
            # Check if we've reached the end
            total_available = data.get('count', 0)
            if total_fetched >= total_available:
                print(f"\nReached end. Total available: {total_available:,}")
                break
            
            # Save progress every 10 pages
            if page % 10 == 0:
                print(f"Saving checkpoint at page {page}...")
                df_temp = pd.DataFrame(all_jobs)
                df_temp.to_csv('data/processed/adzuna_checkpoint.csv', index=False)
            
            page += 1
            
            # Rate limiting - be respectful to the API
            time.sleep(0.5)  # Wait 0.5 seconds between requests
            
            # Safety limit - stop after 400 pages (~20,000 jobs)
            if page > 400:
                print("\nReached safety limit of 400 pages")
                break
                
        except Exception as e:
            print(f"Error: {e}")
            break
    
    print("\n" + "="*50)
    print(f"Collection complete! Total jobs fetched: {len(all_jobs):,}")
    
    return all_jobs

# Run the collection
jobs = fetch_adzuna_jobs()

# Convert to DataFrame
print("\nConverting to DataFrame...")
df = pd.DataFrame(jobs)

# Show summary
print(f"\nTotal rows: {len(df):,}")
print(f"\nColumns: {list(df.columns)}")
print(f"\nDate range:")
print(f"  Earliest: {df['created'].min()}")
print(f"  Latest: {df['created'].max()}")

# Save raw data
print("\nSaving raw Adzuna data...")
df.to_csv('data/processed/adzuna_raw.csv', index=False)
print("Saved to data/processed/adzuna_raw.csv")

print("\nReady to clean and map to unified schema!")

"""
LinkedIn Jobs Data Collection via RapidAPI
Collects data analyst jobs within free tier limits
"""

import requests
import pandas as pd
import time
import json
from datetime import datetime

# Configuration
API_KEY = "ad0938bfc7msh7216e8dc60fb95ep16ac8ajsnca330c79722d"  # Replace with your key
API_HOST = "linkedin-job-search-api.p.rapidapi.com"
OUTPUT_FILE = 'data/raw/linkedin_jobs_rapidapi.csv'

# Search parameters
SEARCH_QUERIES = [
    "data analyst",
    "business analyst",
    "business intelligence analyst"
]

LOCATIONS = [
    "United States",
    # Add more specific locations if needed
]


def search_jobs(query, location="United States", offset=0, limit=100):
    """
    Search for jobs on LinkedIn via RapidAPI
    Uses "Get Jobs 7 days" endpoint
    """
    
    url = f"https://{API_HOST}/active-jb-7d"
    
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }
    
    params = {
        "title_filter": query,
        "location_filter": location,
        "offset": offset,
        "limit": limit
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print(f"[WARNING] Rate limit hit. Waiting 60 seconds...")
            time.sleep(60)
            return None
        else:
            print(f"[ERROR] Status {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print(f"[ERROR] Request failed: {e}")
        return None


def parse_job_data(job):
    """Parse job data into standardized format - matches actual API response"""
    
    # Get location info
    location_raw = job.get('locations_raw', [])
    location = location_raw[0].get('address', {}).get('addressLocality', '') if location_raw else ''
    
    # Get employment type - it's a list of strings like ["FULL_TIME"]
    emp_type = job.get('employment_type', [])
    employment_type = emp_type[0] if emp_type else ''
    
    return {
        'job_id': job.get('id'),
        'title': job.get('title'),
        'company_name': job.get('organization'),
        'location': location,
        'description': job.get('description_text', ''),
        'posted_date': job.get('date_posted'),
        'apply_url': job.get('url'),
        'salary_info': str(job.get('salary_raw', '')),
        'job_type': employment_type,
        'seniority_level': job.get('seniority', ''),
        'company_industry': job.get('linkedin_org_industry', ''),
        'company_size': job.get('linkedin_org_size', ''),
        'source': 'LinkedIn RapidAPI',
        'collected_date': datetime.now().isoformat()
    }


def collect_jobs(max_requests=None):
    """
    Collect jobs within free tier limits
    
    Parameters:
    -----------
    max_requests : int
        Maximum API calls (free tier typically 100-500/month)
        Set to None to collect until rate limit
    """
    
    all_jobs = []
    request_count = 0
    
    print("="*70)
    print("LINKEDIN JOBS COLLECTION")
    print("="*70 + "\n")
    
    for query in SEARCH_QUERIES:
        for location in LOCATIONS:
            
            print(f"\nSearching: '{query}' in '{location}'")
            print("-"*70)
            
            offset = 0
            limit = 100
            
            while True:
                
                # Check if we hit request limit
                if max_requests and request_count >= max_requests:
                    print(f"\n[STOP] Reached max requests ({max_requests})")
                    break
                
                print(f"Offset {offset}...", end=" ")
                
                # Make request
                result = search_jobs(query, location, offset, limit)
                request_count += 1
                
                if result is None:
                    print("Failed")
                    break
                
                # Parse jobs - API returns array directly
                if isinstance(result, list):
                    jobs = result
                else:
                    jobs = result.get('data', [])
                
                if not jobs:
                    print(f"No more results (total: {len(all_jobs)} jobs)")
                    break
                
                # Add to collection
                for job in jobs:
                    parsed = parse_job_data(job)
                    all_jobs.append(parsed)
                
                print(f"Got {len(jobs)} jobs (total: {len(all_jobs)})")
                
                # Rate limiting - be respectful
                time.sleep(2)  # 2 second delay between requests
                
                # Move to next batch
                offset += limit
                
                # Limit iterations to avoid excessive calls
                if offset >= 500:  # Stop after ~500 jobs per query
                    break
            
            if max_requests and request_count >= max_requests:
                break
        
        if max_requests and request_count >= max_requests:
            break
    
    print(f"\n{'='*70}")
    print(f"COLLECTION COMPLETE")
    print(f"{'='*70}")
    print(f"Total requests: {request_count}")
    print(f"Total jobs collected: {len(all_jobs)}")
    
    return all_jobs


def save_results(jobs, output_file):
    """Save collected jobs to CSV"""
    
    if not jobs:
        print("\n[WARNING] No jobs to save")
        return
    
    # Create directory if it doesn't exist
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    df = pd.DataFrame(jobs)
    
    # Remove duplicates
    before = len(df)
    df = df.drop_duplicates(subset=['job_id'])
    after = len(df)
    
    if before > after:
        print(f"\nRemoved {before - after} duplicates")
    
    df.to_csv(output_file, index=False)
    print(f"\n[OK] Saved {len(df)} jobs to {output_file}")
    
    # Show summary
    print(f"\nSummary:")
    print(f"  Unique companies: {df['company_name'].nunique()}")
    print(f"  Unique locations: {df['location'].nunique()}")
    print(f"  Date range: {df['posted_date'].min()} to {df['posted_date'].max()}")


def main():
    """Run collection"""
    
    # Check API key
    if API_KEY == "YOUR_RAPIDAPI_KEY":
        print("[ERROR] Please set your RapidAPI key in the script")
        print("\n1. Go to: https://rapidapi.com/fantastic-jobs-fantastic-jobs-default/api/linkedin-job-search-api")
        print("2. Sign up and subscribe to free tier")
        print("3. Copy your API key")
        print("4. Replace 'YOUR_RAPIDAPI_KEY' in this script\n")
        return
    
    # Collect jobs (adjust max_requests based on your free tier limit)
    # Typical free tiers: 100-500 requests/month
    jobs = collect_jobs(max_requests=100)  # Adjust this number
    
    # Save results
    if jobs:
        save_results(jobs, OUTPUT_FILE)


if __name__ == '__main__':
    main()

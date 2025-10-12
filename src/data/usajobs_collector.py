"""
USAJobs API Collector
Collects federal government data analyst jobs
"""

import requests
import pandas as pd
import time
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class USAJobsCollector:
    def __init__(self):
        self.api_key = os.getenv('USAJOBS_API_KEY')
        self.email = os.getenv('USAJOBS_EMAIL')
        self.base_url = "https://data.usajobs.gov/api/search"
        
        if not self.api_key or not self.email:
            raise ValueError("Missing USAJobs credentials in .env file")
        
        self.headers = {
            "Host": "data.usajobs.gov",
            "User-Agent": self.email,
            "Authorization-Key": self.api_key
        }
    
    def search_jobs(self, keyword="data analyst", results_per_page=500, max_pages=10):
        """Search for jobs and paginate through results"""
        
        all_jobs = []
        page = 1
        
        print(f"Searching USAJobs for: '{keyword}'")
        print("="*60)
        
        while page <= max_pages:
            params = {
                "Keyword": keyword,
                "ResultsPerPage": results_per_page,
                "Page": page
            }
            
            print(f"\nFetching page {page}...", end=" ")
            
            try:
                response = requests.get(
                    self.base_url,
                    headers=self.headers,
                    params=params,
                    timeout=30
                )
                
                if response.status_code != 200:
                    print(f"Error {response.status_code}")
                    break
                
                data = response.json()
                
                # Extract jobs
                search_result = data.get('SearchResult', {})
                jobs = search_result.get('SearchResultItems', [])
                
                if not jobs:
                    print("No more results")
                    break
                
                all_jobs.extend(jobs)
                total_jobs = search_result.get('SearchResultCount', 0)
                
                print(f"Got {len(jobs)} jobs. Total so far: {len(all_jobs)}")
                
                # Check if we've reached the end
                if len(all_jobs) >= total_jobs:
                    print(f"\nReached end. Total available: {total_jobs}")
                    break
                
                page += 1
                
                # Be respectful - small delay between requests
                time.sleep(1)
                
            except Exception as e:
                print(f"Error: {e}")
                break
        
        print("\n" + "="*60)
        print(f"Collection complete! Total jobs: {len(all_jobs)}")
        
        return all_jobs
    
    def parse_jobs(self, raw_jobs):
        """Parse raw API response into clean dataframe"""
        
        print("\nParsing job data...")
        
        parsed_jobs = []
        
        for item in raw_jobs:
            job = item.get('MatchedObjectDescriptor', {})
            
            # Extract position details
            position_title = job.get('PositionTitle', '')
            organization = job.get('OrganizationName', '')
            
            # Location
            locations = job.get('PositionLocation', [])
            location_str = locations[0].get('LocationName', '') if locations else ''
            
            # Salary
            salary_min = None
            salary_max = None
            remuneration = job.get('PositionRemuneration', [])
            if remuneration:
                salary_min = remuneration[0].get('MinimumRange', None)
                salary_max = remuneration[0].get('MaximumRange', None)
            
            # Dates
            pub_start = job.get('PublicationStartDate', '')
            
            # Description
            qualifications = job.get('QualificationSummary', '')
            
            # URL
            url = job.get('PositionURI', '')
            
            parsed_jobs.append({
                'title': position_title,
                'company_name': organization,
                'location': location_str,
                'description': qualifications,
                'posted_date_clean': pub_start[:10] if pub_start else None,
                'salary_min': salary_min,
                'salary_max': salary_max,
                'work_type': 'Not Specified',
                'experience_level': 'Not Specified',
                'skills_text': '',
                'software_text': '',
                'source': 'USAJobs',
                'url': url
            })
        
        df = pd.DataFrame(parsed_jobs)
        
        print(f"Parsed {len(df)} jobs")
        print(f"Jobs with salary: {df['salary_min'].notna().sum()}")
        
        return df

def main():
    collector = USAJobsCollector()
    
    # Collect jobs
    raw_jobs = collector.search_jobs(
        keyword="data analyst",
        results_per_page=500,
        max_pages=20  # Up to 10,000 jobs
    )
    
    # Parse to dataframe
    df = collector.parse_jobs(raw_jobs)
    
    # Save raw data
    output_file = 'data/processed/usajobs_raw.csv'
    df.to_csv(output_file, index=False)
    print(f"\nSaved to: {output_file}")
    
    # Show summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total jobs: {len(df)}")
    print(f"Date range: {df['posted_date_clean'].min()} to {df['posted_date_clean'].max()}")
    print(f"Jobs with salary: {df['salary_min'].notna().sum()}")
    print(f"\nTop 10 agencies:")
    print(df['company_name'].value_counts().head(10))

if __name__ == "__main__":
    main()

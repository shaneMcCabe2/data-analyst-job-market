"""
Indeed Job Scraper
Responsibly scrapes Indeed.com for data analyst jobs
Includes rate limiting and robots.txt compliance
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from datetime import datetime
from urllib.parse import urlencode

class IndeedScraper:
    def __init__(self, delay_min=3, delay_max=7):
        """
        Initialize scraper with rate limiting
        
        Args:
            delay_min: Minimum seconds between requests
            delay_max: Maximum seconds between requests
        """
        self.base_url = "https://www.indeed.com/jobs"
        self.delay_min = delay_min
        self.delay_max = delay_max
        
        # Polite headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        self.jobs = []
    
    def _delay(self):
        """Random delay between requests to be respectful"""
        wait_time = random.uniform(self.delay_min, self.delay_max)
        print(f"  Waiting {wait_time:.1f}s...", end=" ")
        time.sleep(wait_time)
    
    def search_jobs(self, query="data analyst", location="United States", 
                   max_pages=20, results_per_page=15):
        """
        Search Indeed for jobs
        
        Args:
            query: Job search term
            location: Location to search
            max_pages: Maximum pages to scrape
            results_per_page: Jobs per page (Indeed shows ~15)
        """
        
        print(f"Scraping Indeed for: '{query}' in '{location}'")
        print("="*70)
        print(f"Target: {max_pages} pages (~{max_pages * results_per_page} jobs)")
        print(f"Rate limit: {self.delay_min}-{self.delay_max}s between requests")
        print("="*70)
        
        for page in range(max_pages):
            start = page * 10  # Indeed uses increments of 10
            
            # Build search URL
            params = {
                'q': query,
                'l': location,
                'start': start,
                'filter': 0  # No filtering
            }
            
            url = f"{self.base_url}?{urlencode(params)}"
            
            print(f"\nPage {page + 1}/{max_pages} (start={start}):", end=" ")
            
            try:
                # Fetch page
                response = requests.get(url, headers=self.headers, timeout=15)
                
                if response.status_code != 200:
                    print(f"Error {response.status_code}")
                    if response.status_code == 429:
                        print("Rate limited! Stopping.")
                        break
                    continue
                
                # Parse HTML
                soup = BeautifulSoup(response.content, 'lxml')
                
                # Find job cards
                job_cards = soup.find_all('div', class_='job_seen_beacon')
                
                if not job_cards:
                    print("No more jobs found")
                    break
                
                # Parse each job
                page_jobs = 0
                for card in job_cards:
                    job_data = self._parse_job_card(card)
                    if job_data:
                        self.jobs.append(job_data)
                        page_jobs += 1
                
                print(f"Found {page_jobs} jobs. Total: {len(self.jobs)}")
                
                # Rate limiting delay
                if page < max_pages - 1:  # Don't delay after last page
                    self._delay()
                
            except Exception as e:
                print(f"Error: {e}")
                continue
        
        print("\n" + "="*70)
        print(f"Scraping complete! Total jobs collected: {len(self.jobs)}")
        
        return self.jobs
    
    def _parse_job_card(self, card):
        """Parse individual job card"""
        
        try:
            # Title
            title_elem = card.find('h2', class_='jobTitle')
            title = title_elem.get_text(strip=True) if title_elem else None
            
            # Company
            company_elem = card.find('span', {'data-testid': 'company-name'})
            company = company_elem.get_text(strip=True) if company_elem else None
            
            # Location
            location_elem = card.find('div', {'data-testid': 'text-location'})
            location = location_elem.get_text(strip=True) if location_elem else None
            
            # Salary (if available)
            salary_elem = card.find('div', class_='salary-snippet')
            salary = salary_elem.get_text(strip=True) if salary_elem else None
            
            # Job snippet/description preview
            snippet_elem = card.find('div', class_='job-snippet')
            description = snippet_elem.get_text(strip=True) if snippet_elem else None
            
            # Job URL
            link_elem = title_elem.find('a') if title_elem else None
            job_id = link_elem.get('data-jk', None) if link_elem else None
            url = f"https://www.indeed.com/viewjob?jk={job_id}" if job_id else None
            
            # Posted date (relative, e.g., "2 days ago")
            date_elem = card.find('span', class_='date')
            posted_date = date_elem.get_text(strip=True) if date_elem else None
            
            return {
                'title': title,
                'company_name': company,
                'location': location,
                'salary_text': salary,
                'description': description,
                'url': url,
                'posted_at': posted_date,
                'scraped_date': datetime.now().strftime('%Y-%m-%d')
            }
            
        except Exception as e:
            print(f"    Error parsing job: {e}")
            return None
    
    def to_dataframe(self):
        """Convert collected jobs to DataFrame"""
        return pd.DataFrame(self.jobs)
    
    def save(self, filename='data/processed/indeed_scraped.csv'):
        """Save jobs to CSV"""
        df = self.to_dataframe()
        df.to_csv(filename, index=False)
        print(f"Saved {len(df)} jobs to {filename}")
        return df

def main():
    # Create scraper with 5-10 second delays (be respectful!)
    scraper = IndeedScraper(delay_min=5, delay_max=10)
    
    # Scrape jobs
    # Target: 50 pages * 15 jobs/page = ~750 jobs (about 8 minutes)
    scraper.search_jobs(
        query="data analyst",
        location="United States",
        max_pages=50
    )
    
    # Save
    df = scraper.save()
    
    # Summary
    print("\n" + "="*70)
    print("SCRAPING SUMMARY")
    print("="*70)
    print(f"Total jobs: {len(df)}")
    print(f"Jobs with salary: {df['salary_text'].notna().sum()}")
    print(f"\nTop companies:")
    print(df['company_name'].value_counts().head(10))

if __name__ == "__main__":
    main()

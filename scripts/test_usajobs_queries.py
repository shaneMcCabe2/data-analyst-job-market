"""Test different USAJobs search queries"""

import os
from dotenv import load_dotenv
import requests

load_dotenv()

api_key = os.getenv('USAJOBS_API_KEY')
email = os.getenv('USAJOBS_EMAIL')

headers = {
    "Host": "data.usajobs.gov",
    "User-Agent": email,
    "Authorization-Key": api_key
}

base_url = "https://data.usajobs.gov/api/search"

# Test different keywords
keywords = [
    "data analyst",
    "data",
    "analyst", 
    "business analyst",
    "intelligence analyst",
    "management analyst",
    "program analyst"
]

print("Testing USAJobs search queries...")
print("="*60)

for keyword in keywords:
    params = {
        "Keyword": keyword,
        "ResultsPerPage": 500
    }
    
    response = requests.get(base_url, headers=headers, params=params)
    data = response.json()
    
    count = data.get('SearchResult', {}).get('SearchResultCount', 0)
    print(f"{keyword:30} -> {count:,} jobs")
print("="*60)
print("\nTry the keyword with the most results!")

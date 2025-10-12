# Data Sources Documentation

## Overview

This project combines data from multiple sources to create a comprehensive dataset of U.S. data analyst job postings from 2024-2025.

## Final Dataset Statistics

- **Total Jobs:** 46,610 (after deduplication)
- **Date Range:** January 2024 - October 2025
- **Geography:** United States only
- **Jobs with Salary:** 11,720 (25.1%)
- **Remote Jobs:** 18,026 (38.7%)

---

## Data Sources

### 1. Adzuna API (Primary Source)

**Collection Date:** October 2025  
**Method:** REST API  
**Jobs Collected:** 16,350 (5,507 after deduplication)  
**Date Range:** October 3-11, 2025

**Strengths:**
- 100% salary data completeness
- Real-time current data
- Clean, structured API responses

**API Details:**
- Endpoint: https://api.adzuna.com/v1/api/jobs/us/search/
- Rate Limit: 5,000 calls/month (free tier)

**Code:** `src/data/fetch_adzuna_data.py`

---

### 2. Google Search Jobs (Kaggle Dataset)

**Collection Date:** April 2025  
**Method:** Kaggle dataset download  
**Jobs Collected:** 61,912 (39,342 after deduplication)  
**Date Range:** March-April 2025

**Strengths:**
- Large volume
- Includes salary data (15% of jobs)
- Recent 2025 data

**Challenges Fixed:**
- Mixed hourly/annual salaries (converted hourly * 2080)
- Inconsistent location formats (normalized)

**Dataset:** `lukebarousse/data-analyst-job-postings-google-search`  
**Code:** `src/data/clean_google_data.py`

---

### 3. LinkedIn Job Postings (Kaggle)

**3a. LinkedIn Data Jobs (2025)**
- Jobs: 844 (791 after deduplication)
- Date: April 2025
- Dataset: `joykimaiyo18/linkedin-data-jobs-dataset`

**3b. LinkedIn USA (2022)**
- Jobs: 2,845 (205 after deduplication)
- Date: November 2022
- Work types labeled: Onsite/Remote/Hybrid
- Dataset: `cedricaubin/linkedin-data-analyst-jobs-listings`

**Code:** `src/data/clean_linkedin_data.py`, `src/data/clean_linkedin_usa.py`

---

### 4. Indeed (2024 Historical - Kaggle)

**Collection Date:** Throughout 2024  
**Method:** Kaggle dataset (biweekly scrapes)  
**Jobs Collected:** 13,761 (738 after deduplication)  
**Date Range:** January - December 2024

**Strengths:**
- Full year monthly coverage
- Consistent data quality

**Dataset:** `artemfedorov/vacancies-from-indeed-scraped-biweekly-2024`  
**Code:** `src/data/clean_indeed_2024.py`

---

### 5. USAJobs API

**Collection Date:** October 2025  
**Method:** Government REST API  
**Jobs Collected:** 28 (27 after deduplication)  
**Date Range:** June - October 2025

**Strengths:**
- 100% salary data
- Federal government positions
- Official government source
- Unlimited free API access

**Limitations:**
- Only federal jobs (limited volume)
- Different job title conventions

**API:** https://developer.usajobs.gov/  
**Code:** `src/data/usajobs_collector.py`

---

## Data Processing Pipeline

### Deduplication Process

**Method:** Fuzzy matching on normalized fields

**Normalization:**
- Company names: Remove Inc, LLC, Corp suffixes
- Job titles: Remove level indicators (I, II, Senior, Junior)
- Locations: Standardize format

**Results:**
- Original: 95,740 jobs
- After deduplication: 46,610 jobs (51% were duplicates)

**Code:** `scripts/deduplicate_final.py`, `src/data/deduplication.py`

### Feature Engineering

**Added Features:**
1. **State extraction** from location strings
2. **Experience level** from job titles (Entry/Mid/Senior)
3. **Salary average** calculation
4. **Date features** (year, month, quarter)
5. **Derived flags** (is_remote, has_salary)
6. **Skills/software counts**

**Code:** `scripts/final_data_preparation.py`

---

## Data Quality

### Completeness by Field

- Title: 100%
- Company: 100%
- Location: 100%
- State: 63.5% (Remote: 38.5%, Unknown: 35.0%)
- Salary: 25.1%
- Experience Level: 99.9%
- Posted Date: 13.5%

### Known Limitations

1. **Date coverage limited:** Only 6,272 jobs (13.5%) have valid posted dates
2. **Geographic unknowns:** 35% of locations couldn't be mapped to states
3. **Salary data:** Only 25% of jobs include salary information
4. **Skills extraction:** Pending NLP analysis phase

---

## Ethical Considerations

### Data Collection Ethics

**APIs:**
- Stayed within free tier rate limits
- Proper attribution of all sources
- No data reselling or redistribution

**Web Scraping Attempt:**
- Indeed blocked scraping attempts (403 errors)
- Respected anti-scraping protections
- Did not circumvent blocking mechanisms

**Privacy:**
- Only publicly posted job listings
- No personally identifiable information
- Aggregated analysis only

---

## File Locations

**Raw Data:** `data/raw/` (gitignored)

**Processed Data:**
- Individual cleaned sources: `data/processed/*_cleaned.csv`
- Combined dataset: `data/processed/jobs_all_combined.csv`
- Final deduplicated: `data/processed/jobs_final_deduplicated.csv`
- Analysis-ready: `data/processed/jobs_analysis_ready.csv` (CURRENT)

**Database:** `data/job_market.db` (SQLite)

---

## Data Version

**Current Version:** 1.0  
**Last Updated:** October 11, 2025  
**Status:** Analysis-ready

See `data/DATA_VERSION.txt` for details.

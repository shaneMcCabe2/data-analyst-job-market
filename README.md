# Data Analyst Job Market Analysis (2025)

A comprehensive data science project analyzing the U.S. data analyst job market using 46,610 job postings from multiple sources. Demonstrates end-to-end data pipeline development, statistical analysis, and machine learning techniques.

**Status:** Data collection and cleaning complete. Analysis phase in progress.

---

## Project Overview

**Research Questions:**
- What are the salary trends by experience level and location?
- Which technical skills are most in-demand?
- How does remote work impact compensation?
- Can we predict salaries based on job characteristics?
- What insights can NLP reveal from job descriptions?

**Dataset:**
- 46,610 unique job postings (deduplicated from 95,740)
- 11,720 jobs with salary data (25.1%)
- Date range: January 2024 - October 2025
- Geography: United States

---

## Key Technologies

**Data Collection:**
- REST APIs (Adzuna, USAJobs)
- Kaggle datasets (Google Jobs, LinkedIn, Indeed)
- Python: requests, BeautifulSoup

**Data Processing:**
- Python: pandas, numpy
- SQLite database
- Fuzzy matching for deduplication
- Feature engineering

**Planned Analysis:**
- Statistical testing (t-tests, ANOVA)
- Machine Learning (Random Forest, XGBoost)
- NLP (spaCy, topic modeling)
- Visualization (Plotly, interactive dashboards)

---

## Project Structure

data-analyst-job-market/
├── src/
│   ├── data/                 # Data collection & cleaning modules
│   │   ├── clean_.py       # Source-specific cleaning
│   │   ├── deduplication.py # Fuzzy matching
│   │   ├── fetch_.py       # API collectors
│   │   └── *_scraper.py     # Web scrapers
│   ├── features/            # Feature engineering (planned)
│   ├── models/              # ML models (planned)
│   └── utils/               # Helper functions (planned)
├── scripts/                 # Executable scripts
│   ├── data.py           # Data processing
│   └── chart.py          # Visualization generation
├── notebooks/               # Jupyter analysis (planned)
├── data/
│   ├── raw/                # Original downloads (gitignored)
│   └── processed/          # Cleaned data (gitignored)
│       └── jobs_analysis_ready.csv  # CURRENT DATASET
├── docs/                   # Documentation
│   ├── DATA_SOURCES.md    # Data collection details
│   └── ANALYSIS_ROADMAP.md # Analysis plan
├── visualizations/         # Output charts
│   └── salary_by_experience.html
├── archive/                # Old/test files
├── .env                   # API keys (gitignored)
├── Pipfile                # Dependencies
└── README.md

---

## Current Progress

**Phase 1: Data Collection & Cleaning** - COMPLETE
- [x] Collected 95,740 jobs from 5 sources
- [x] Implemented fuzzy matching deduplication
- [x] Extracted experience levels from job titles
- [x] Parsed geographic data (states)
- [x] Standardized salary formats
- [x] Created analysis-ready dataset (46,610 jobs)

**Phase 2: Exploratory Data Analysis** - IN PROGRESS
- [ ] Salary distributions by experience/location
- [ ] Skills frequency analysis
- [ ] Remote vs onsite patterns
- [ ] Geographic visualizations

**Phase 3: Statistical Analysis** - PLANNED
- [ ] Hypothesis testing (salary comparisons)
- [ ] Correlation analysis (skills vs salary)

**Phase 4: Machine Learning** - PLANNED
- [ ] Salary prediction models
- [ ] Feature importance analysis
- [ ] Model comparison

**Phase 5: NLP Analysis** - PLANNED
- [ ] Skills extraction from descriptions
- [ ] Topic modeling
- [ ] Text classification

**Phase 6: Dashboard** - PLANNED
- [ ] Interactive Plotly/Streamlit dashboard

---

## Quick Start

### Prerequisites
```bash
# Python 3.12+
python --version

# Install pipenv
pip install pipenv

Installation

# Clone repository
git clone [your-repo-url]
cd data-analyst-job-market

# Install dependencies
pipenv install

# Activate environment
pipenv shell


Setup API Keys (Optional - only if collecting new data)

bash# Create .env file
cp .env.example .env

# Add your API keys:
# RAPIDAPI_KEY=your_key
# ADZUNA_APP_ID=your_id
# ADZUNA_APP_KEY=your_key
# USAJOBS_API_KEY=your_key
# USAJOBS_EMAIL=your_email

Use Existing Data
The cleaned, analysis-ready dataset is available at:
data/processed/jobs_analysis_ready.csv

Data Sources
Data collected from:

Adzuna API - 16,350 jobs (Oct 2025)
Google Jobs - 61,912 jobs (Apr 2025)
LinkedIn - 3,689 jobs (2022-2025)
Indeed - 13,761 jobs (2024)
USAJobs - 28 jobs (2025)

After deduplication: 46,610 unique jobs
See DATA_SOURCES.md for detailed information.

Sample Visualizations
Salary by Experience Level (2025 Data):

Average salaries:

Entry Level: $72,933
Mid Level: $92,958
Senior Level: $125,717

More visualizations coming in analysis phase.

Documentation

Data Sources - Detailed source information
Analysis Roadmap - Planned analyses and methods


Contributing
This is a portfolio project. Feedback and suggestions are welcome via issues.

License
This project is for educational and portfolio purposes.

Contact
[Your Name]

LinkedIn: [your-profile]
Portfolio: [your-website]
Email: [your-email]


Acknowledgments
Data sources:

Adzuna API
USAJobs.gov API
Kaggle datasets by lukebarousse, joykimaiyo18, cedricaubin, artemfedorov
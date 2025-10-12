# Analysis Roadmap

This document outlines the statistical analysis and machine learning techniques to apply to the job market dataset.

## Current Dataset

- **Total Jobs:** 46,610 unique positions
- **Salary Data:** 11,720 jobs (25.1%)
- **Time Period:** January 2024 - October 2025
- **Geography:** United States
- **Experience Levels:** Entry (3%), Mid (75%), Senior (22%)

---

## Phase 1: Exploratory Data Analysis (EDA)

**Goal:** Understand data distributions and relationships

**Analyses:**
1. Salary distribution by experience level
2. Geographic distribution of jobs
3. Remote vs onsite trends over time
4. Top hiring companies
5. Skills frequency analysis
6. Correlation matrix (salary, experience, location, skills)

**Deliverables:**
- Jupyter notebook: `notebooks/01_eda.ipynb`
- Key visualizations saved to `visualizations/`

**Tools:** pandas, matplotlib, seaborn, plotly

---

## Phase 2: Statistical Analysis

**Goal:** Test hypotheses about the job market

### Analysis 2.1: Salary Hypothesis Testing

**Questions:**
- Does remote work pay differently than onsite? (t-test)
- Are salary differences across regions significant? (ANOVA)
- Has average salary changed from 2024 to 2025? (t-test)

**Methods:**
- Two-sample t-tests
- ANOVA with post-hoc tests
- Effect size calculations (Cohen's d)
- Confidence intervals

**Code:** `notebooks/02_hypothesis_testing.ipynb`

### Analysis 2.2: Correlation Analysis

**Questions:**
- Which skills correlate most with higher salaries?
- Do certain skill combinations predict higher pay?
- Is experience level the strongest salary predictor?

**Methods:**
- Pearson/Spearman correlation
- Partial correlation (controlling for experience)
- Correlation heatmaps

**Code:** `notebooks/02_hypothesis_testing.ipynb`

---

## Phase 3: Machine Learning - Salary Prediction

**Goal:** Build predictive models for salary estimation

### Model 3.1: Linear Regression (Baseline)

**Features:**
- Experience level (ordinal encoding)
- Location (state, or one-hot encoding)
- Skills (binary: has Python, has SQL, etc.)
- Work type (remote/onsite/hybrid)

**Evaluation:**
- R-squared
- RMSE
- MAE
- Feature importance

### Model 3.2: Random Forest Regressor

**Why:** Handles non-linear relationships, feature interactions

**Features:** Same as above + engineered features:
- Skill count
- Tech stack diversity
- Company size (if available)

### Model 3.3: XGBoost (Best Performance)

**Why:** State-of-the-art for tabular data

**Hyperparameter Tuning:**
- Grid search or Bayesian optimization
- Cross-validation (5-fold)

**Deliverables:**
- Model comparison notebook: `notebooks/03_salary_prediction.ipynb`
- Trained models saved to: `src/models/`
- Feature importance visualizations

---

## Phase 4: NLP Analysis

**Goal:** Extract insights from job descriptions

### Analysis 4.1: Skills Extraction

**Method:**
- Named Entity Recognition (NER) with spaCy
- Custom entity recognition for technical skills
- Keyword extraction

**Output:**
- Skills frequency ranking
- Skills co-occurrence network
- Skills by experience level

### Analysis 4.2: Topic Modeling

**Method:** Latent Dirichlet Allocation (LDA)

**Goal:** Find hidden topics in job descriptions

**Examples:**
- "Data Visualization" topic
- "Machine Learning" topic
- "Business Analytics" topic

**Compare:** Topics by experience level, salary tier

### Analysis 4.3: Text Classification

**Task:** Predict experience level from job description

**Method:**
- TF-IDF vectorization
- Logistic Regression / Naive Bayes
- Evaluation: Accuracy, F1-score, confusion matrix

**Deliverables:**
- NLP notebook: `notebooks/05_nlp_analysis.ipynb`
- Skills network visualization
- Topic distribution charts

---

## Phase 5: Advanced Techniques

### Analysis 5.1: Clustering

**Goal:** Group similar jobs

**Method:** K-means or DBSCAN

**Features:**
- Salary
- Skills (one-hot encoded)
- Location
- Description embeddings (optional: BERT)

**Output:**
- Job clusters (e.g., "Entry Data Viz", "Senior ML Engineer")
- Cluster characteristics
- Silhouette score

### Analysis 5.2: Geographic Analysis

**Goal:** Understand regional patterns

**Analyses:**
- Cost-of-living adjusted salaries
- Choropleth maps (salary by state)
- Urban vs rural differences
- Salary hotspots

**Tools:** Folium, Plotly geographic plots

### Analysis 5.3: Time Series Analysis

**Goal:** Identify trends over time

**Analyses:**
- Job posting volume trends
- Salary trends (2024 vs 2025)
- Seasonal patterns
- Skills demand changes

**Methods:**
- Moving averages
- Trend decomposition
- Prophet forecasting (optional)

**Code:** `notebooks/06_time_series.ipynb`

---

## Phase 6: Interactive Dashboard

**Goal:** Professional interactive visualization

**Tool:** Plotly Dash or Streamlit

**Features:**
- Filters: Experience level, location, date range, skills
- Charts: Salary distribution, skills ranking, geographic map
- Search: Find jobs matching criteria
- Export: Download filtered data

**Deployment:** Streamlit Cloud (free hosting)

**Code:** `src/dashboard/app.py`

---

## Recommended Implementation Order

**Week 1:**
1. EDA (Phase 1)
2. Hypothesis testing (Phase 2)
3. Salary prediction - baseline (Phase 3.1)

**Week 2:**
4. Advanced ML models (Phase 3.2, 3.3)
5. Skills extraction (Phase 4.1)
6. Clustering (Phase 5.1)

**Week 3:**
7. Topic modeling (Phase 4.2)
8. Geographic analysis (Phase 5.2)
9. Interactive dashboard (Phase 6)

---

## Key Deliverables for Portfolio

**Minimum for strong portfolio:**
1. Salary prediction model with feature importance
2. Hypothesis testing with clear findings
3. Skills network visualization
4. 3-5 polished interactive charts
5. Well-documented README

**Bonus impressive additions:**
1. Interactive dashboard
2. Topic modeling insights
3. Clustering analysis
4. Time series forecasting

---

## Tools & Libraries Needed
```bash
# Install analysis tools
pipenv install scikit-learn xgboost
pipenv install spacy
pipenv install wordcloud
pipenv install plotly dash streamlit
pipenv install statsmodels scipy
pipenv install folium

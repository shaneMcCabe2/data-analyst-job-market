# Data Analyst Job Market Analysis

## Business Problem
With 200,000+ monthly data analyst job postings, candidates lack clear guidance on which skills deliver salary returns and optimal career progression strategies.

## Analysis Approach
Analyzed 46,000+ job postings using:
- **Data cleaning**: Custom deduplication algorithm reducing dataset by 40% while preserving data integrity
- **Statistical modeling**: Correlation analysis and partial correlation to isolate skill value from experience effects
- **Predictive modeling**: Random Forest to identify non-linear skill interactions

## Key Insights

**Experience drives base salary**, but specific skills add measurable premiums:
- Python: +$9,608 (11.6% premium)
- Snowflake: +$13,252 (16.0% premium)  
- AWS: +$16,952 (20.5% premium)

**Python's value is independent** - maintains strong correlation (r=0.21) even after controlling for experience, unlike most skills that correlate primarily through experience.

**Career progression math**: Entry → Senior yields +$38K (45.9%), but skill acquisition can accelerate progression by targeting high-premium technologies.

## Technical Implementation

**Stack**: Python (Pandas, Plotly, SciPy) | Statistical Analysis (Pearson/Spearman correlation, partial correlation, Random Forest)

**Methodology highlights**:
- Implemented fuzzy matching algorithm for company name standardization
- Developed percentile-based outlier detection (preserved 95th percentile, removed clear errors)
- Used partial correlation to isolate skill effects from experience confounding

## Repository Structure
```
├── notebooks/          # Full analysis with methodology
├── data/              # Raw and processed datasets  
├── src/               # Reusable analysis functions
└── outputs/           # Final visualizations
```

## Sample Outputs


<img width="700" height="500" alt="image" src="https://github.com/user-attachments/assets/3b990cb4-c675-4de2-b3ae-926c3f9b2692" />

<img width="1123" height="1016" alt="image" src="https://github.com/user-attachments/assets/5ad24a2f-b346-4bf6-afaf-0a0bd83f331d" />

<img width="700" height="600" alt="image" src="https://github.com/user-attachments/assets/0382642c-acef-46f0-98c8-94c6ce011802" />  




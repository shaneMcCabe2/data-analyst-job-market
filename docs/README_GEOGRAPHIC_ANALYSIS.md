# Geographic Salary Analysis - Getting Started Guide

This folder contains everything you need to create stunning US map visualizations showing data analyst salaries by region and state.

## 📁 Files Overview

1. **`salary_geographic_analysis.ipynb`** - Comprehensive Jupyter notebook with all analysis code
2. **`run_geographic_analysis.py`** - Standalone Python script to run the full analysis
3. **`generate_sample_data.py`** - Create sample data for testing (if you don't have your data ready yet)

## 🚀 Quick Start

### Option 1: Using Sample Data (Test First)

If you want to test the visualizations before loading your actual data:

```bash
# 1. Generate sample data
python generate_sample_data.py

# 2. Run the analysis (make sure DATA_PATH points to the sample data)
python run_geographic_analysis.py
```

This will create:
- Interactive HTML maps in `outputs/visualizations/`
- CSV summaries of regional and state statistics
- Console output with key findings

### Option 2: Using Your Actual Data

**Step 1: Prepare Your Data**

Your CSV file should have these columns (at minimum):
- `location` or `state` - State abbreviation (e.g., "CA", "NY", "MA")
- `salary_min` and `salary_max` OR `salary_avg`
- Optional but helpful: `experience_level`, `remote_type`, `job_title`, `company_size`

Example data structure:
```csv
job_id,job_title,state,salary_min,salary_max,experience_level,remote_type
JOB_001,Data Analyst,CA,80000,100000,Mid,Remote
JOB_002,Senior Data Analyst,NY,95000,120000,Senior,Hybrid
```

**Step 2: Update Configuration**

In `run_geographic_analysis.py`, change line 17:
```python
DATA_PATH = 'data/job_postings.csv'  # Update to your actual file path
```

**Step 3: Run the Analysis**

```bash
python run_geographic_analysis.py
```

### Option 3: Using Jupyter Notebook (Interactive)

If you prefer working in a notebook environment:

```bash
# 1. Start Jupyter
jupyter notebook

# 2. Open salary_geographic_analysis.ipynb

# 3. Update the data loading cell with your file path

# 4. Run all cells
```

## 📊 What You'll Get

The analysis generates these visualizations:

1. **Interactive US Choropleth Map** (`salary_map_by_state.html`)
   - Color-coded states by average salary
   - Hover to see details
   - Zoom and pan enabled

2. **Regional Comparison Bar Chart** (`regional_comparison.html`)
   - Compare Northeast, South, Midwest, West
   - Shows mean and median salaries side-by-side

3. **Top States Ranking** (`top_states.html`)
   - Horizontal bar chart of highest-paying states
   - Color-coded by salary level

4. **Job Volume vs Salary Scatter** (`volume_vs_salary.html`)
   - Identify "sweet spot" states (high salary + high volume)
   - Sized by number of jobs

5. **Summary Statistics** (CSV files)
   - `regional_summary.csv` - Regional averages, medians, ranges
   - `state_summary.csv` - State-by-state breakdown

## 📋 Requirements

Install required packages:

```bash
pip install pandas numpy plotly jupyter
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

## 🎨 Customization Options

### Change the Map Color Scheme

In `run_geographic_analysis.py` or the notebook, find:
```python
color_continuous_scale='RdYlGn'
```

Change to other Plotly color scales:
- `'Viridis'` - Blue to yellow gradient
- `'Blues'` - Light to dark blue
- `'Plasma'` - Purple to yellow
- `'RdBu'` - Red to blue (diverging)

### Adjust the Number of Top States Shown

In `run_geographic_analysis.py`, line 287:
```python
top_n=15  # Change this number
```

### Filter by Experience Level

If your data has an `experience_level` column, add this after loading:
```python
df = df[df['experience_level'] == 'Entry']  # Only entry-level jobs
```

## 🔍 Understanding the Regional Classifications

States are grouped using US Census Bureau regions:

- **Northeast**: CT, ME, MA, NH, RI, VT, NJ, NY, PA
- **Midwest**: IL, IN, MI, OH, WI, IA, KS, MN, MO, NE, ND, SD
- **South**: DE, FL, GA, MD, NC, SC, VA, WV, AL, KY, MS, TN, AR, LA, OK, TX
- **West**: AZ, CO, ID, MT, NV, NM, UT, WY, AK, CA, HI, OR, WA

## 📈 Analysis Tips

### Finding the Best Markets

Look for states in the **top-right quadrant** of the scatter plot:
- High salary (Y-axis)
- High job volume (X-axis)
- These are your target markets!

### Identifying Geographic Arbitrage Opportunities

Compare:
1. **Remote positions** in high-paying states
2. **Your current location** salary
3. Potential for **geographic arbitrage** (live in low COL, earn high salary remotely)

### Understanding Regional Trends

- **West Coast** typically shows highest salaries (tech hubs)
- **Northeast** strong for finance/insurance sectors
- **Midwest** stable, slightly lower salaries but also lower cost of living
- **South** fast-growing markets, competitive salaries

## 🐛 Troubleshooting

**Issue**: "No state column found"
- **Solution**: Make sure your location data includes state abbreviations, or update the extraction logic

**Issue**: "No module named 'plotly'"
- **Solution**: Install plotly: `pip install plotly`

**Issue**: "All salaries showing as $0"
- **Solution**: Check that salary columns are numeric, not strings

**Issue**: "Map shows no data"
- **Solution**: Verify state abbreviations are 2-letter codes (e.g., "CA" not "California")

**Issue**: "Too many outliers removed"
- **Solution**: Adjust the quantile thresholds in the data cleaning section

## 📊 Next Steps

After completing geographic analysis:

1. **Skills Analysis** - Which skills pay more in each region?
2. **Remote vs Onsite** - Salary differences by work type
3. **Time Series** - How have salaries changed over time?
4. **Company Size** - Startup vs enterprise compensation

## 💡 Tips for Your Portfolio

When presenting this analysis:

1. **Start with the map** - It's the most visually striking
2. **Tell a story** - "I analyzed 46K jobs and found..."
3. **Highlight actionable insights** - "For someone in NH, remote roles in CA offer 30% higher salaries"
4. **Show your process** - Include code snippets in your README
5. **Make it interactive** - Host the HTML visualizations on GitHub Pages

## 📞 Questions?

If you run into issues or want to extend the analysis, just ask!

---

*Created for the Data Analyst Job Market Analysis project*

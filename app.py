"""
Data Analyst Job Market Dashboard
Interactive Streamlit dashboard showcasing key insights from job market analysis
"""

import streamlit as st
import plotly.graph_objects as go
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Data Analyst Job Market Insights",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .insight-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
        color: #2c3e50;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Select Section:",
    ["Executive Summary", "Skills Analysis", "Geographic Insights", "Experience & Salary", "Methodology"]
)

# Base path for visualizations
VIZ_PATH = Path("outputs/visualizations")

def load_html_viz(filename):
    """Load and display HTML visualization"""
    file_path = VIZ_PATH / filename
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def display_viz_with_insight(viz_file, insight_title, insight_text):
    """Display visualization with accompanying insight box"""
    st.markdown(f'<div class="sub-header">{insight_title}</div>', unsafe_allow_html=True)
    
    # Display insight
    st.markdown(f"""
        <div class="insight-box">
            <strong>Key Insight:</strong> {insight_text}
        </div>
    """, unsafe_allow_html=True)
    
    # Display visualization
    html_content = load_html_viz(viz_file)
    if html_content:
        st.components.v1.html(html_content, height=600, scrolling=True)
    else:
        st.warning(f"Visualization {viz_file} not found")

# Main content based on selected page
if page == "Executive Summary":
    st.markdown('<div class="main-header">Data Analyst Job Market Analysis</div>', unsafe_allow_html=True)
    st.markdown("### Comprehensive analysis of 46,000+ job postings")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Job Postings Analyzed",
            value="46,000+",
            delta="40% after deduplication"
        )
    
    with col2:
        st.metric(
            label="Python Salary Premium",
            value="+$9,608",
            delta="11.6% increase"
        )
    
    with col3:
        st.metric(
            label="AWS Salary Premium",
            value="+$16,952",
            delta="20.5% increase"
        )
    
    with col4:
        st.metric(
            label="Entry → Senior Increase",
            value="+$38,000",
            delta="45.9% growth"
        )
    
    st.markdown("---")
    
    # Business problem
    st.markdown('<div class="sub-header">Business Problem</div>', unsafe_allow_html=True)
    st.markdown("""
    With over 200,000 monthly data analyst job postings, candidates face a critical challenge: 
    **which skills actually deliver salary returns and enable optimal career progression?**
    
    This analysis provides data-driven answers by examining real job market trends.
    """)
    
    # Key findings
    st.markdown('<div class="sub-header">Key Findings</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box">
        <strong>1. Experience is the Foundation</strong><br>
        Base salary correlates most strongly with years of experience, with entry to senior progression 
        yielding an average increase of $38,000 (45.9%).
    </div>
    
    <div class="insight-box">
        <strong>2. Specific Skills Add Measurable Premiums</strong><br>
        • Python: +$9,608 (11.6% premium)<br>
        • Snowflake: +$13,252 (16.0% premium)<br>
        • AWS: +$16,952 (20.5% premium)
    </div>
    
    <div class="insight-box">
        <strong>3. Python's Independent Value</strong><br>
        Python maintains strong correlation (r=0.21) even after controlling for experience effects, 
        unlike most skills that correlate primarily through experience confounding.
    </div>
    
    <div class="insight-box">
        <strong>4. Strategic Skill Acquisition Accelerates Career Growth</strong><br>
        Targeting high-premium technologies (cloud platforms, modern data tools) can significantly 
        accelerate progression beyond experience alone.
    </div>
    """, unsafe_allow_html=True)

elif page == "Skills Analysis":
    st.markdown('<div class="main-header">Skills & Salary Analysis</div>', unsafe_allow_html=True)
    
    # Top skills visualization
    display_viz_with_insight(
        "top_skills_bar.html",
        "Most In-Demand Skills",
        """SQL and Excel dominate job requirements, appearing in 60%+ of postings. However, 
        cloud platforms (AWS, Azure) and modern data tools (Snowflake, Databricks) command 
        significantly higher salary premiums despite lower posting frequency - indicating high 
        value for specialized skills."""
    )
    
    st.markdown("---")
    
    # Skills by category
    display_viz_with_insight(
        "skills_by_category.html",
        "Skills Distribution by Category",
        """Programming languages and BI tools form the foundation of data analyst roles, but 
        cloud platforms and databases are rapidly growing in importance. The shift toward 
        cloud-based analytics stacks is clear in hiring requirements."""
    )
    
    st.markdown("---")
    
    # Correlation heatmap (if you have it as PNG)
    st.markdown('<div class="sub-header">Skill Correlation Analysis</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="insight-box">
            <strong>Key Insight:</strong> Strong correlations exist between cloud platforms (AWS, Azure, GCP) 
            and modern data tools (Snowflake, Databricks), suggesting these skills cluster together in 
            data engineering-focused roles with higher compensation.
        </div>
    """, unsafe_allow_html=True)
    
    # Display PNG if it exists
    png_path = VIZ_PATH / "correlation_heatmap.png"
    if png_path.exists():
        st.image(str(png_path), use_container_width=True)

elif page == "Geographic Insights":
    st.markdown('<div class="main-header">Geographic Trends</div>', unsafe_allow_html=True)
    
    # State-level analysis
    display_viz_with_insight(
        "salary_map_by_state.html",
        "Salary Distribution by State",
        """California, New York, and Washington lead in both job volume and median salaries, 
        driven by tech hub concentration. However, remote work trends are creating opportunities 
        for competitive salaries outside traditional tech centers.
        
        Note: The chosen datasets lacked significant geographic data. For future versions, 
        collecting more geographic data is needed to draw stronger conclusions on geographic differences."""
    )
    
    st.markdown("---")
    
    # Top states
    display_viz_with_insight(
        "top_states.html",
        "States with Highest Job Posting Volume",
        """Geographic concentration in tech hubs remains strong, but the rise of remote positions 
        (56% of analyzed postings) is democratizing access to high-paying data analyst roles 
        across geographic boundaries."""
    )

elif page == "Experience & Salary":
    st.markdown('<div class="main-header">Experience Level & Compensation</div>', unsafe_allow_html=True)
    
    # Experience distribution
    display_viz_with_insight(
        "experience_level_bar.html",
        "Job Postings by Experience Level",
        """Mid-level and senior positions dominate the market, indicating employers prioritize 
        proven experience. Entry-level opportunities exist but are more competitive, emphasizing 
        the value of portfolio projects and demonstrable skills for career entry."""
    )
    
    st.markdown("---")
    
    # Salary by experience (HTML version)
    display_viz_with_insight(
        "salary_by_experience.html",
        "Salary Progression by Experience",
        """Clear salary progression exists across experience levels: Entry ($83K median) → 
        Mid ($95K) → Senior ($121K). The $38K jump from entry to senior represents a 45.9% 
        increase, but skill acquisition in high-premium technologies can accelerate this timeline."""
    )
    
    st.markdown("---")
    
    # Work type analysis
    display_viz_with_insight(
        "work_type_pie.html",
        "Distribution by Work Arrangement",
        """Remote work has fundamentally changed the data analyst market. Fully remote positions 
        now represent a significant portion of opportunities, with hybrid arrangements also common. 
        This shift expands the addressable job market for candidates regardless of location."""
    )

elif page == "Methodology":
    st.markdown('<div class="main-header">Analysis Methodology</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Data Collection & Processing
    
    **Dataset Composition:**
    - 46,000+ unique job postings after deduplication
    - 40% reduction through custom fuzzy matching algorithm
    - Preserved data integrity while removing duplicates
    
    **Data Sources:**
    - Multiple job posting APIs and aggregators
    - Standardized company names using fuzzy matching
    - Validated salary data using percentile-based outlier detection
    
    ### Statistical Methods
    
    **Correlation Analysis:**
    - Pearson correlation for linear relationships
    - Spearman correlation for non-linear patterns
    - Partial correlation to isolate skill effects from experience confounding
    
    **Predictive Modeling:**
    - Random Forest regression to identify non-linear skill interactions
    - Feature importance ranking to quantify skill value
    - Cross-validation to ensure model generalization
    
    **Outlier Treatment:**
    - Preserved 95th percentile to capture legitimate high earners
    - Removed only clear data entry errors (e.g., $1M+ salaries)
    - Maintained realistic salary distributions
    
    ### Key Findings Validation
    
    All reported salary premiums were validated through:
    1. Statistical significance testing (p < 0.05)
    2. Multiple correlation methods (Pearson, Spearman, partial)
    3. Machine learning model confirmation (Random Forest)
    
    ### Technical Stack
    
    **Languages & Libraries:**
    - Python (Pandas, NumPy, SciPy, Scikit-learn)
    - Plotly for interactive visualizations
    - Streamlit for dashboard deployment
    
    **Analysis Tools:**
    - Jupyter Notebooks for exploratory analysis
    - PostgreSQL for data storage
    - Git for version control
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ### Repository Structure
    
    ```
    ├── notebooks/              # Full analysis notebooks
    ├── data/                   # Raw and processed datasets
    ├── src/                    # Reusable analysis modules
    ├── outputs/visualizations/ # Generated charts
    ├── scripts/                # ETL and data collection
    └── app.py                  # This Streamlit dashboard
    ```
    
    **[View Full Analysis on GitHub](https://github.com/shaneMcCabe2/data-analyst-job-market)**
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <strong>Shane McCabe</strong> | 
        <a href='https://github.com/shaneMcCabe2'>GitHub</a> | 
        <a href='https://www.linkedin.com/in/shane-mccabe-54aaa239a/'>LinkedIn</a><br>
        Built with Python, Plotly, and Streamlit
    </div>
""", unsafe_allow_html=True)
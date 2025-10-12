"""
Geographic Salary Analysis - Main Runner Script
This script loads your job data and runs the geographic analysis
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ============================================================================
# CONFIGURATION - UPDATE THESE PATHS
# ============================================================================

# Path to your job data CSV
DATA_PATH = 'data/processed/jobs_analysis_ready.csv'

# Output directory for visualizations
OUTPUT_DIR = 'outputs/visualizations'
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

# US Census Bureau regional definitions
US_REGIONS = {
    'Northeast': ['CT', 'ME', 'MA', 'NH', 'RI', 'VT', 'NJ', 'NY', 'PA', 'DC'],
    'Midwest': ['IL', 'IN', 'MI', 'OH', 'WI', 'IA', 'KS', 'MN', 'MO', 'NE', 'ND', 'SD'],
    'South': ['DE', 'FL', 'GA', 'MD', 'NC', 'SC', 'VA', 'WV', 'AL', 'KY', 'MS', 'TN', 
              'AR', 'LA', 'OK', 'TX'],
    'West': ['AZ', 'CO', 'ID', 'MT', 'NV', 'NM', 'UT', 'WY', 'AK', 'CA', 'HI', 'OR', 'WA']
}

STATE_TO_REGION = {}
for region, states in US_REGIONS.items():
    for state in states:
        STATE_TO_REGION[state] = region


def load_and_prepare_data(file_path):
    """
    Load job data and prepare it for analysis
    
    Expected columns in your CSV:
    - location or state (state abbreviation)
    - salary_min and salary_max OR salary_avg
    - Other columns: job_title, experience_level, remote_type, etc.
    """
    print(f"Loading data from {file_path}...")
    df = pd.read_csv(file_path, low_memory=False)
    
    print(f"Loaded {len(df):,} job postings")
    print(f"Columns: {', '.join(df.columns)}")
    
    # Calculate average salary if needed
    if 'salary_avg' not in df.columns:
        if 'salary_min' in df.columns and 'salary_max' in df.columns:
            df['salary_avg'] = (df['salary_min'] + df['salary_max']) / 2
            print("[OK] Calculated salary_avg from min and max")
    
    # Extract state abbreviation if needed
    if 'state' not in df.columns and 'location' in df.columns:
        # Try to extract 2-letter state code from location string
        df['state'] = df['location'].str.extract(r'([A-Z]{2})')[0]
        print("[OK] Extracted state from location column")
    
    # Add region
    if 'state' in df.columns:
        df['region'] = df['state'].map(STATE_TO_REGION)
        print("[OK] Added region classification")
        
        # Filter out invalid states (Unknown, Remote, etc.) but keep valid nulls
        invalid_states = ['Unknown', 'Remote', 'unknown', 'remote', '']
        df = df[~df['state'].isin(invalid_states)]
        
        # Show states with no region match
        missing_regions = df[df['region'].isna()]['state'].unique()
        if len(missing_regions) > 0:
            print(f"[WARNING] Warning: {len(missing_regions)} states with no region match: {missing_regions}")
    
    # Only remove rows missing BOTH salary and state
    before_count = len(df)
    df = df.dropna(subset=['salary_avg', 'state', 'region'])
    after_count = len(df)
    
    if before_count > after_count:
        print(f"[WARNING] Removed {before_count - after_count:,} rows with missing salary or state data")
    
    # Remove salary outliers
    q1 = df['salary_avg'].quantile(0.01)
    q99 = df['salary_avg'].quantile(0.99)
    df = df[(df['salary_avg'] >= q1) & (df['salary_avg'] <= q99)]
    print(f"[OK] Filtered to {len(df):,} jobs after outlier removal")
    print(f"  Salary range: ${df['salary_avg'].min():,.0f} - ${df['salary_avg'].max():,.0f}")
    
    return df


def calculate_statistics(df, min_jobs_per_state=20):
    """Calculate regional and state-level statistics"""
    
    # Filter to states with sufficient data
    state_counts = df['state'].value_counts()
    valid_states = state_counts[state_counts >= min_jobs_per_state].index
    df_filtered = df[df['state'].isin(valid_states)].copy()
    
    removed_states = len(state_counts) - len(valid_states)
    if removed_states > 0:
        print(f"[WARNING] Excluded {removed_states} states with <{min_jobs_per_state} salary data points")
        print(f"[WARNING] Analysis includes {len(valid_states)} states with sufficient data")
    
    # Regional stats
    regional_stats = df_filtered.groupby('region').agg({
        'salary_avg': ['mean', 'median', 'std', 'min', 'max'],
        'title': 'count'
    }).round(0)
    regional_stats.columns = ['mean_salary', 'median_salary', 'std_salary', 
                               'min_salary', 'max_salary', 'job_count']
    regional_stats = regional_stats.reset_index()
    regional_stats = regional_stats.sort_values('mean_salary', ascending=False)
    
    # State stats
    state_stats = df_filtered.groupby('state').agg({
        'salary_avg': ['mean', 'median', 'count'],
        'region': 'first'
    }).round(0)
    state_stats.columns = ['mean_salary', 'median_salary', 'job_count', 'region']
    state_stats = state_stats.reset_index()
    
    return regional_stats, state_stats


def create_choropleth_map(state_stats, output_path=None):
    """Create interactive US map showing salary by state"""
    
    fig = px.choropleth(
        state_stats,
        locations='state',
        locationmode='USA-states',
        color='mean_salary',
        hover_name='state',
        hover_data={
            'state': False,
            'mean_salary': ':$,.0f',
            'job_count': ':,',
            'region': True
        },
        color_continuous_scale='RdYlGn',
        scope='usa',
        title='Data Analyst Average Salary by State (Limited Data - States with 10+ Jobs)',
        labels={'mean_salary': 'Avg Salary ($)'}
    )
    
    fig.update_layout(
        geo=dict(
            showlakes=True,
            lakecolor='rgb(255, 255, 255)'
        ),
        height=600,
        title_font_size=20
    )
    
    if output_path:
        fig.write_html(output_path)
        print(f"[OK] Saved choropleth map to {output_path}")
    
    return fig


def create_regional_bars(regional_stats, output_path=None):
    """Create bar chart comparing regions"""
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=regional_stats['region'],
        y=regional_stats['mean_salary'],
        name='Mean Salary',
        marker_color='lightblue',
        text=regional_stats['mean_salary'].apply(lambda x: f'${x:,.0f}'),
        textposition='outside'
    ))
    
    fig.add_trace(go.Bar(
        x=regional_stats['region'],
        y=regional_stats['median_salary'],
        name='Median Salary',
        marker_color='coral',
        text=regional_stats['median_salary'].apply(lambda x: f'${x:,.0f}'),
        textposition='outside'
    ))
    
    fig.update_layout(
        title='Average Data Analyst Salary by US Region',
        xaxis_title='Region',
        yaxis_title='Salary ($)',
        barmode='group',
        height=500,
        showlegend=True
    )
    
    if output_path:
        fig.write_html(output_path)
        print(f"[OK] Saved regional bar chart to {output_path}")
    
    return fig


def create_top_states_chart(state_stats, top_n=15, output_path=None):
    """Create horizontal bar chart of top paying states"""
    
    top_states = state_stats.nlargest(top_n, 'mean_salary')
    
    fig = go.Figure(go.Bar(
        x=top_states['mean_salary'],
        y=top_states['state'],
        orientation='h',
        marker=dict(
            color=top_states['mean_salary'],
            colorscale='Viridis',
            showscale=True
        ),
        text=top_states['mean_salary'].apply(lambda x: f'${x:,.0f}'),
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Avg Salary: $%{x:,.0f}<br>Jobs: %{customdata}',
        customdata=top_states['job_count']
    ))
    
    fig.update_layout(
        title=f'Top {top_n} States by Average Data Analyst Salary',
        xaxis_title='Average Salary ($)',
        yaxis_title='State',
        height=600,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    if output_path:
        fig.write_html(output_path)
        print(f"[OK] Saved top states chart to {output_path}")
    
    return fig


def create_scatter_plot(state_stats, output_path=None):
    """Create scatter plot showing job volume vs salary"""
    
    fig = px.scatter(
        state_stats,
        x='job_count',
        y='mean_salary',
        size='job_count',
        color='region',
        hover_name='state',
        hover_data={'job_count': ':,', 'mean_salary': ':$,.0f'},
        title='Job Volume vs Average Salary by State',
        labels={'job_count': 'Number of Jobs', 'mean_salary': 'Average Salary ($)'},
        size_max=40
    )
    
    fig.update_layout(height=600)
    
    if output_path:
        fig.write_html(output_path)
        print(f"[OK] Saved scatter plot to {output_path}")
    
    return fig


def print_summary(regional_stats, state_stats, total_jobs_analyzed):
    """Print text summary of findings"""
    
    print("\n" + "="*70)
    print("GEOGRAPHIC SALARY ANALYSIS SUMMARY (LIMITED DATA)")
    print("="*70)
    print(f"\nNOTE: Analysis based on {total_jobs_analyzed:,} jobs with complete salary data")
    print("This represents a subset of the full dataset. Results may not be representative.")
    print("="*70)
    
    print("\nREGIONAL RANKINGS (by mean salary):")
    print("-" * 70)
    for idx, row in regional_stats.iterrows():
        print(f"{row['region']:12} | ${row['mean_salary']:>8,.0f} avg | "
              f"${row['median_salary']:>8,.0f} median | {row['job_count']:>6,} jobs")
    
    print("\nTOP 10 STATES (by mean salary):")
    print("-" * 70)
    top_10 = state_stats.nlargest(10, 'mean_salary')
    for idx, row in top_10.iterrows():
        print(f"{row['state']:3} ({row['region']:9}) | ${row['mean_salary']:>8,.0f} avg | "
              f"{row['job_count']:>5,} jobs")
    
    print("\nSTATES WITH MOST JOBS:")
    print("-" * 70)
    top_volume = state_stats.nlargest(10, 'job_count')
    for idx, row in top_volume.iterrows():
        print(f"{row['state']:3} ({row['region']:9}) | {row['job_count']:>5,} jobs | "
              f"${row['mean_salary']:>8,.0f} avg")
    
    print("\n" + "="*70 + "\n")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run the complete geographic analysis"""
    
    print("="*70)
    print("DATA ANALYST JOB MARKET: GEOGRAPHIC SALARY ANALYSIS")
    print("="*70 + "\n")
    
    # 1. Load and prepare data
    try:
        df = load_and_prepare_data(DATA_PATH)
    except FileNotFoundError:
        print(f"\n[ERROR] Error: Could not find file at {DATA_PATH}")
        print("Please update DATA_PATH at the top of this script to point to your data file.")
        return
    except Exception as e:
        print(f"\n[ERROR] Error loading data: {e}")
        return
    
    # 2. Calculate statistics
    print("\nCalculating statistics...")
    regional_stats, state_stats = calculate_statistics(df, min_jobs_per_state=10)
    
    # 3. Create visualizations
    print("\nCreating visualizations...")
    
    choropleth = create_choropleth_map(
        state_stats, 
        f'{OUTPUT_DIR}/salary_map_by_state.html'
    )
    
    regional_bars = create_regional_bars(
        regional_stats,
        f'{OUTPUT_DIR}/regional_comparison.html'
    )
    
    top_states = create_top_states_chart(
        state_stats,
        top_n=15,
        output_path=f'{OUTPUT_DIR}/top_states.html'
    )
    
    scatter = create_scatter_plot(
        state_stats,
        f'{OUTPUT_DIR}/volume_vs_salary.html'
    )
    
    # 4. Save summary data
    print("\nSaving summary data...")
    regional_stats.to_csv(f'{OUTPUT_DIR}/regional_summary.csv', index=False)
    state_stats.to_csv(f'{OUTPUT_DIR}/state_summary.csv', index=False)
    print(f"[OK] Saved CSV summaries to {OUTPUT_DIR}/")
    
    # 5. Print text summary
    print_summary(regional_stats, state_stats, len(df))
    
    # 6. Show interactive plots (optional - comment out if running headless)
    print("Opening visualizations in browser...")
    choropleth.show()
    
    print("\n[DONE] Analysis complete! Check the outputs/ folder for all visualizations.")
    print("\nNOTE: This analysis uses only jobs with complete salary and location data.")
    print("For more comprehensive geographic analysis, consider analysis based on job counts only.")


if __name__ == '__main__':
    main()

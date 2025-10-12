"""
Remote vs Onsite Work Analysis
Analyzes work type distribution and patterns
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Configuration
INPUT_FILE = 'data/processed/jobs_with_work_type_v2.csv'
OUTPUT_DIR = 'outputs/visualizations'

# Dark theme
DARK_THEME = {
    'plot_bgcolor': '#1e1e1e',
    'paper_bgcolor': '#2d2d2d',
    'font_color': '#e0e0e0',
    'gridcolor': '#404040'
}


def load_and_prepare(file_path):
    """Load data and prepare work type columns"""
    
    print(f"Loading data from {file_path}...")
    df = pd.read_csv(file_path, low_memory=False)
    print(f"Loaded {len(df):,} jobs\n")
    
    # Check available columns
    has_work_type = 'work_type' in df.columns
    has_is_remote = 'is_remote' in df.columns
    
    if not has_work_type and not has_is_remote:
        print("[ERROR] No work type columns found")
        return None
    
    # Create standardized work_type if needed
    if has_is_remote and not has_work_type:
        df['work_type'] = df['is_remote'].apply(lambda x: 'Remote' if x else 'Onsite')
    
    # Clean work_type values
    df['work_type'] = df['work_type'].fillna('Unknown')
    df['work_type'] = df['work_type'].str.title()
    
    # Filter out Not Specified
    before_filter = len(df)
    df = df[df['work_type'] != 'Not Specified'].copy()
    after_filter = len(df)
    
    print(f"Filtered out {before_filter - after_filter:,} 'Not Specified' jobs")
    print(f"Analyzing {after_filter:,} jobs with specified work types\n")
    
    return df


def analyze_by_source(df):
    """Compare work type distribution across sources"""
    
    # Create crosstab with percentages
    source_work_counts = pd.crosstab(df['source'], df['work_type'])
    source_work_pct = pd.crosstab(df['source'], df['work_type'], normalize='index') * 100
    source_work_pct = source_work_pct.round(1)
    
    print("="*70)
    print("WORK TYPE DISTRIBUTION BY SOURCE")
    print("="*70)
    
    for source in source_work_counts.index:
        total = source_work_counts.loc[source].sum()
        print(f"\n{source} (n={total:,}):")
        for work_type in source_work_counts.columns:
            count = source_work_counts.loc[source, work_type]
            pct = source_work_pct.loc[source, work_type]
            print(f"  {work_type:15} | {count:6,} ({pct:5.1f}%)")
    
    print("="*70 + "\n")
    
    return source_work_counts, source_work_pct


def create_source_comparison_chart(source_work_pct):
    """Create stacked bar chart comparing sources"""
    
    fig = go.Figure()
    
    colors = {'Remote': '#4CAF50', 'Hybrid': '#FFC107', 'Onsite': '#2196F3'}
    
    for work_type in source_work_pct.columns:
        fig.add_trace(go.Bar(
            name=work_type,
            x=source_work_pct.index,
            y=source_work_pct[work_type],
            marker_color=colors.get(work_type, '#9E9E9E'),
            text=source_work_pct[work_type].apply(lambda x: f'{x:.0f}%'),
            textposition='inside',
            textfont=dict(color='white')
        ))
    
    fig.update_layout(
        title='Work Type Distribution by Data Source',
        xaxis_title='Data Source',
        yaxis_title='Percentage of Jobs',
        barmode='stack',
        height=500,
        plot_bgcolor=DARK_THEME['plot_bgcolor'],
        paper_bgcolor=DARK_THEME['paper_bgcolor'],
        font=dict(color=DARK_THEME['font_color']),
        xaxis=dict(gridcolor=DARK_THEME['gridcolor']),
        yaxis=dict(gridcolor=DARK_THEME['gridcolor'])
    )
    
    return fig


def create_source_grouped_chart(source_work_pct):
    """Create grouped bar chart for easier comparison"""
    
    fig = go.Figure()
    
    colors = {'Remote': '#4CAF50', 'Hybrid': '#FFC107', 'Onsite': '#2196F3'}
    
    for work_type in source_work_pct.columns:
        fig.add_trace(go.Bar(
            name=work_type,
            x=source_work_pct.index,
            y=source_work_pct[work_type],
            marker_color=colors.get(work_type, '#9E9E9E'),
            text=source_work_pct[work_type].apply(lambda x: f'{x:.0f}%'),
            textposition='outside',
            textfont=dict(color=DARK_THEME['font_color'])
        ))
    
    fig.update_layout(
        title='Work Type Comparison Across Data Sources',
        xaxis_title='Data Source',
        yaxis_title='Percentage of Jobs',
        barmode='group',
        height=500,
        plot_bgcolor=DARK_THEME['plot_bgcolor'],
        paper_bgcolor=DARK_THEME['paper_bgcolor'],
        font=dict(color=DARK_THEME['font_color']),
        xaxis=dict(gridcolor=DARK_THEME['gridcolor']),
        yaxis=dict(gridcolor=DARK_THEME['gridcolor'])
    )
    
    return fig


def analyze_work_type_distribution(df):
    """Analyze distribution of work types"""
    
    work_counts = df['work_type'].value_counts()
    work_pct = (work_counts / len(df) * 100).round(1)
    
    print("="*70)
    print("WORK TYPE DISTRIBUTION")
    print("="*70)
    for work_type, count in work_counts.items():
        pct = work_pct[work_type]
        print(f"{work_type:15} | {count:6,} jobs ({pct:5.1f}%)")
    print("="*70 + "\n")
    
    return work_counts, work_pct


def create_work_type_pie(work_counts):
    """Create pie chart of work type distribution"""
    
    fig = go.Figure(data=[go.Pie(
        labels=work_counts.index,
        values=work_counts.values,
        hole=0.3,
        marker=dict(colors=['#4CAF50', '#FFC107', '#2196F3', '#9E9E9E']),
        textinfo='label+percent',
        textfont=dict(size=14, color='white'),
        hovertemplate='<b>%{label}</b><br>%{value:,} jobs<br>%{percent}'
    )])
    
    fig.update_layout(
        title='Job Distribution by Work Type',
        paper_bgcolor=DARK_THEME['paper_bgcolor'],
        font=dict(color=DARK_THEME['font_color'], size=12),
        height=500,
        showlegend=True
    )
    
    return fig


def create_work_type_bar(work_counts):
    """Create bar chart of work types"""
    
    df_plot = pd.DataFrame({
        'work_type': work_counts.index,
        'count': work_counts.values,
        'percentage': (work_counts.values / work_counts.sum() * 100).round(1)
    })
    
    fig = go.Figure(go.Bar(
        x=df_plot['count'],
        y=df_plot['work_type'],
        orientation='h',
        marker_color='#4CAF50',
        text=df_plot.apply(lambda x: f"{x['count']:,} ({x['percentage']:.1f}%)", axis=1),
        textposition='outside',
        textfont=dict(color=DARK_THEME['font_color'])
    ))
    
    fig.update_layout(
        title='Job Count by Work Type',
        xaxis_title='Number of Jobs',
        yaxis_title='',
        height=400,
        plot_bgcolor=DARK_THEME['plot_bgcolor'],
        paper_bgcolor=DARK_THEME['paper_bgcolor'],
        font=dict(color=DARK_THEME['font_color']),
        xaxis=dict(gridcolor=DARK_THEME['gridcolor']),
        yaxis=dict(gridcolor=DARK_THEME['gridcolor'], ticksuffix='  ')
    )
    
    return fig


def analyze_work_type_by_state(df):
    """Analyze work type distribution by state"""
    
    # Get top 15 states by job count
    top_states = df['state'].value_counts().head(15).index
    df_top = df[df['state'].isin(top_states)].copy()
    
    # Create pivot table
    pivot = pd.crosstab(df_top['state'], df_top['work_type'], normalize='index') * 100
    pivot = pivot.round(1)
    
    return pivot


def create_state_work_type_heatmap(pivot):
    """Create heatmap showing work type % by state"""
    
    # Sort states by remote percentage
    if 'Remote' in pivot.columns:
        pivot = pivot.sort_values('Remote', ascending=False)
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale='Viridis',
        text=pivot.values,
        texttemplate='%{text:.0f}%',
        textfont=dict(size=10),
        hovertemplate='<b>%{y}</b><br>%{x}: %{z:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title='Work Type Distribution by State (Top 15 States)',
        xaxis_title='Work Type',
        yaxis_title='',
        height=600,
        paper_bgcolor=DARK_THEME['paper_bgcolor'],
        font=dict(color=DARK_THEME['font_color']),
        xaxis=dict(side='top'),
        yaxis=dict(ticksuffix='  ')
    )
    
    return fig


def analyze_remote_trends_over_time(df):
    """Analyze how remote work has changed over time"""
    
    if 'year' not in df.columns and 'posted_date_clean' not in df.columns:
        print("[WARNING] No date columns available for trend analysis")
        return None
    
    # Use year if available, otherwise extract from date
    if 'year' in df.columns:
        df['year_col'] = df['year']
    else:
        df['year_col'] = pd.to_datetime(df['posted_date_clean'], errors='coerce').dt.year
    
    # Remove nulls and unrealistic years
    df = df[df['year_col'].notna()]
    df = df[(df['year_col'] >= 2020) & (df['year_col'] <= 2025)]
    
    # Calculate percentages by year
    trend = df.groupby(['year_col', 'work_type']).size().reset_index(name='count')
    totals = df.groupby('year_col').size().reset_index(name='total')
    trend = trend.merge(totals, on='year_col')
    trend['percentage'] = (trend['count'] / trend['total'] * 100).round(1)
    
    return trend


def create_trend_line_chart(trend_df):
    """Create line chart showing work type trends over time"""
    
    fig = px.line(
        trend_df,
        x='year_col',
        y='percentage',
        color='work_type',
        markers=True,
        title='Work Type Trends Over Time',
        labels={'year_col': 'Year', 'percentage': 'Percentage of Jobs', 'work_type': 'Work Type'}
    )
    
    fig.update_layout(
        height=500,
        plot_bgcolor=DARK_THEME['plot_bgcolor'],
        paper_bgcolor=DARK_THEME['paper_bgcolor'],
        font=dict(color=DARK_THEME['font_color']),
        xaxis=dict(gridcolor=DARK_THEME['gridcolor']),
        yaxis=dict(gridcolor=DARK_THEME['gridcolor'])
    )
    
    return fig


def analyze_salary_by_work_type(df):
    """Compare salaries across work types"""
    
    if 'salary_avg' not in df.columns:
        print("[WARNING] No salary data available")
        return None
    
    # Filter to jobs with salary data
    df_salary = df[df['salary_avg'].notna()].copy()
    
    if len(df_salary) < 100:
        print(f"[WARNING] Only {len(df_salary)} jobs with salary data - results may not be representative")
        return None
    
    salary_stats = df_salary.groupby('work_type')['salary_avg'].agg(['mean', 'median', 'count']).round(0)
    salary_stats.columns = ['mean_salary', 'median_salary', 'job_count']
    salary_stats = salary_stats.sort_values('mean_salary', ascending=False)
    
    print("SALARY BY WORK TYPE")
    print("="*70)
    for work_type, row in salary_stats.iterrows():
        print(f"{work_type:15} | ${row['mean_salary']:>8,.0f} avg | ${row['median_salary']:>8,.0f} median | {row['job_count']:>4,.0f} jobs")
    print("="*70 + "\n")
    
    return salary_stats


def create_salary_comparison_chart(salary_stats):
    """Create bar chart comparing salaries by work type"""
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Mean Salary',
        x=salary_stats.index,
        y=salary_stats['mean_salary'],
        marker_color='#4CAF50',
        text=salary_stats['mean_salary'].apply(lambda x: f'${x:,.0f}'),
        textposition='outside',
        textfont=dict(color=DARK_THEME['font_color'])
    ))
    
    fig.add_trace(go.Bar(
        name='Median Salary',
        x=salary_stats.index,
        y=salary_stats['median_salary'],
        marker_color='#FFC107',
        text=salary_stats['median_salary'].apply(lambda x: f'${x:,.0f}'),
        textposition='outside',
        textfont=dict(color=DARK_THEME['font_color'])
    ))
    
    fig.update_layout(
        title='Average Salary by Work Type',
        xaxis_title='Work Type',
        yaxis_title='Salary ($)',
        barmode='group',
        height=500,
        plot_bgcolor=DARK_THEME['plot_bgcolor'],
        paper_bgcolor=DARK_THEME['paper_bgcolor'],
        font=dict(color=DARK_THEME['font_color']),
        xaxis=dict(gridcolor=DARK_THEME['gridcolor']),
        yaxis=dict(gridcolor=DARK_THEME['gridcolor'])
    )
    
    return fig


def main():
    """Run complete remote vs onsite analysis"""
    
    print("="*70)
    print("REMOTE VS ONSITE WORK ANALYSIS")
    print("="*70 + "\n")
    
    # Load data
    df = load_and_prepare(INPUT_FILE)
    if df is None:
        return
    
    # 1. Distribution analysis
    work_counts, work_pct = analyze_work_type_distribution(df)
    
    # 1b. Source comparison
    source_counts, source_pct = analyze_by_source(df)
    
    # 2. Create visualizations
    print("Creating visualizations...\n")
    
    # Pie chart
    fig1 = create_work_type_pie(work_counts)
    fig1.write_html(f'{OUTPUT_DIR}/work_type_pie.html')
    print(f"[OK] Saved: {OUTPUT_DIR}/work_type_pie.html")
    
    # Bar chart
    fig2 = create_work_type_bar(work_counts)
    fig2.write_html(f'{OUTPUT_DIR}/work_type_bar.html')
    print(f"[OK] Saved: {OUTPUT_DIR}/work_type_bar.html")
    
    # State heatmap
    pivot = analyze_work_type_by_state(df)
    fig3 = create_state_work_type_heatmap(pivot)
    fig3.write_html(f'{OUTPUT_DIR}/work_type_by_state.html')
    print(f"[OK] Saved: {OUTPUT_DIR}/work_type_by_state.html")
    
    # Source comparison - stacked
    fig_src1 = create_source_comparison_chart(source_pct)
    fig_src1.write_html(f'{OUTPUT_DIR}/work_type_by_source_stacked.html')
    print(f"[OK] Saved: {OUTPUT_DIR}/work_type_by_source_stacked.html")
    
    # Source comparison - grouped
    fig_src2 = create_source_grouped_chart(source_pct)
    fig_src2.write_html(f'{OUTPUT_DIR}/work_type_by_source_grouped.html')
    print(f"[OK] Saved: {OUTPUT_DIR}/work_type_by_source_grouped.html")
    
    # Trend analysis
    trend_df = analyze_remote_trends_over_time(df)
    if trend_df is not None:
        fig4 = create_trend_line_chart(trend_df)
        fig4.write_html(f'{OUTPUT_DIR}/work_type_trends.html')
        print(f"[OK] Saved: {OUTPUT_DIR}/work_type_trends.html")
    
    # Salary comparison
    salary_stats = analyze_salary_by_work_type(df)
    if salary_stats is not None:
        fig5 = create_salary_comparison_chart(salary_stats)
        fig5.write_html(f'{OUTPUT_DIR}/salary_by_work_type.html')
        print(f"[OK] Saved: {OUTPUT_DIR}/salary_by_work_type.html")
    
    print("\n[DONE] Analysis complete!")
    print(f"All visualizations saved to {OUTPUT_DIR}/")
    
    # Open main chart
    fig1.show()


if __name__ == '__main__':
    main()

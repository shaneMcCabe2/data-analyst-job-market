"""
Experience Level Analysis
Analyzes job distribution by seniority/experience level
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Configuration
INPUT_FILE = 'data/processed/jobs_2025_only.csv'
OUTPUT_DIR = 'outputs/visualizations'

# Dark theme
DARK_THEME = {
    'plot_bgcolor': '#1e1e1e',
    'paper_bgcolor': '#2d2d2d',
    'font_color': '#e0e0e0',
    'gridcolor': '#404040'
}


def load_and_prepare(file_path):
    """Load data and clean experience level column"""
    
    print(f"Loading data from {file_path}...")
    df = pd.read_csv(file_path, low_memory=False)
    print(f"Loaded {len(df):,} jobs\n")
    
    if 'experience_level' not in df.columns:
        print("[ERROR] No experience_level column found")
        return None
    
    # Clean and standardize
    df['experience_level'] = df['experience_level'].fillna('Not Specified')
    df['experience_level'] = df['experience_level'].str.title()
    
    return df


def analyze_distribution(df):
    """Analyze experience level distribution"""
    
    exp_counts = df['experience_level'].value_counts()
    exp_pct = (exp_counts / len(df) * 100).round(1)
    
    print("="*70)
    print("EXPERIENCE LEVEL DISTRIBUTION")
    print("="*70)
    for level, count in exp_counts.items():
        pct = exp_pct[level]
        print(f"{level:20} | {count:6,} jobs ({pct:5.1f}%)")
    print("="*70 + "\n")
    
    return exp_counts, exp_pct


def create_experience_pie(exp_counts):
    """Create pie chart of experience levels"""
    
    fig = go.Figure(data=[go.Pie(
        labels=exp_counts.index,
        values=exp_counts.values,
        hole=0.3,
        marker=dict(colors=['#4CAF50', '#FFC107', '#2196F3', '#FF5722', '#9E9E9E']),
        textinfo='label+percent',
        textfont=dict(size=12, color='white'),
        hovertemplate='<b>%{label}</b><br>%{value:,} jobs<br>%{percent}'
    )])
    
    fig.update_layout(
        title='Job Distribution by Experience Level',
        paper_bgcolor=DARK_THEME['paper_bgcolor'],
        font=dict(color=DARK_THEME['font_color']),
        height=500
    )
    
    return fig


def create_experience_bar(exp_counts):
    """Create bar chart"""
    
    df_plot = pd.DataFrame({
        'level': exp_counts.index,
        'count': exp_counts.values,
        'percentage': (exp_counts.values / exp_counts.sum() * 100).round(1)
    }).sort_values('count', ascending=True)
    
    fig = go.Figure(go.Bar(
        x=df_plot['count'],
        y=df_plot['level'],
        orientation='h',
        marker_color='#4CAF50',
        text=df_plot.apply(lambda x: f"{x['count']:,} ({x['percentage']:.1f}%)", axis=1),
        textposition='outside',
        textfont=dict(color=DARK_THEME['font_color'])
    ))
    
    fig.update_layout(
        title='Job Count by Experience Level',
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


def analyze_by_work_type(df):
    """Analyze experience level distribution by work type"""
    
    if 'work_type' not in df.columns:
        print("[WARNING] No work_type column - skipping work type analysis")
        return None
    
    # Filter out Not Specified
    df_filtered = df[
        (df['work_type'] != 'Not Specified') & 
        (df['experience_level'] != 'Not Specified')
    ].copy()
    
    if len(df_filtered) < 100:
        print("[WARNING] Insufficient data for work type comparison")
        return None
    
    # Create crosstab
    crosstab = pd.crosstab(df_filtered['work_type'], df_filtered['experience_level'], normalize='index') * 100
    crosstab = crosstab.round(1)
    
    print("EXPERIENCE LEVEL BY WORK TYPE (%):")
    print("="*70)
    print(crosstab)
    print("="*70 + "\n")
    
    return crosstab


def create_work_type_comparison(crosstab):
    """Create stacked bar chart comparing work types"""
    
    fig = go.Figure()
    
    colors = {
        'Entry Level': '#4CAF50',
        'Mid Level': '#FFC107', 
        'Senior Level': '#2196F3',
        'Lead': '#FF5722',
        'Executive': '#9C27B0'
    }
    
    for level in crosstab.columns:
        fig.add_trace(go.Bar(
            name=level,
            x=crosstab.index,
            y=crosstab[level],
            marker_color=colors.get(level, '#9E9E9E'),
            text=crosstab[level].apply(lambda x: f'{x:.0f}%' if x > 5 else ''),
            textposition='inside',
            textfont=dict(color='white')
        ))
    
    fig.update_layout(
        title='Experience Level Distribution by Work Type',
        xaxis_title='Work Type',
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


def analyze_by_state(df):
    """Analyze experience levels by state"""
    
    if 'state' not in df.columns:
        return None
    
    # Get top 10 states
    top_states = df['state'].value_counts().head(10).index
    df_top = df[
        (df['state'].isin(top_states)) & 
        (df['experience_level'] != 'Not Specified')
    ].copy()
    
    if len(df_top) < 100:
        return None
    
    # Create pivot
    pivot = pd.crosstab(df_top['state'], df_top['experience_level'], normalize='index') * 100
    pivot = pivot.round(1)
    
    # Sort by entry level %
    if 'Entry Level' in pivot.columns:
        pivot = pivot.sort_values('Entry Level', ascending=False)
    
    return pivot


def create_state_heatmap(pivot):
    """Create heatmap of experience by state"""
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale='Viridis',
        text=pivot.values,
        texttemplate='%{text:.0f}%',
        textfont=dict(size=9),
        hovertemplate='<b>%{y}</b><br>%{x}: %{z:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title='Experience Level Distribution by State (Top 10)',
        xaxis_title='Experience Level',
        yaxis_title='',
        height=500,
        paper_bgcolor=DARK_THEME['paper_bgcolor'],
        font=dict(color=DARK_THEME['font_color']),
        xaxis=dict(side='top'),
        yaxis=dict(ticksuffix='  ')
    )
    
    return fig


def main():
    """Run complete experience level analysis"""
    
    print("="*70)
    print("EXPERIENCE LEVEL ANALYSIS")
    print("="*70 + "\n")
    
    # Load data
    df = load_and_prepare(INPUT_FILE)
    if df is None:
        return
    
    # 1. Overall distribution
    exp_counts, exp_pct = analyze_distribution(df)
    
    # 2. Create visualizations
    print("Creating visualizations...\n")
    
    # Pie chart
    fig1 = create_experience_pie(exp_counts)
    fig1.write_html(f'{OUTPUT_DIR}/experience_level_pie.html')
    print(f"[OK] Saved: {OUTPUT_DIR}/experience_level_pie.html")
    
    # Bar chart
    fig2 = create_experience_bar(exp_counts)
    fig2.write_html(f'{OUTPUT_DIR}/experience_level_bar.html')
    print(f"[OK] Saved: {OUTPUT_DIR}/experience_level_bar.html")
    
    # Work type comparison
    crosstab = analyze_by_work_type(df)
    if crosstab is not None:
        fig3 = create_work_type_comparison(crosstab)
        fig3.write_html(f'{OUTPUT_DIR}/experience_by_work_type.html')
        print(f"[OK] Saved: {OUTPUT_DIR}/experience_by_work_type.html")
    
    # State heatmap
    state_pivot = analyze_by_state(df)
    if state_pivot is not None:
        fig4 = create_state_heatmap(state_pivot)
        fig4.write_html(f'{OUTPUT_DIR}/experience_by_state.html')
        print(f"[OK] Saved: {OUTPUT_DIR}/experience_by_state.html")
    
    print("\n[DONE] Experience level analysis complete!")
    print(f"All visualizations saved to {OUTPUT_DIR}/")
    
    # Open main chart
    fig1.show()


if __name__ == '__main__':
    main()

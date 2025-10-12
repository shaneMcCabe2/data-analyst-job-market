"""
Skills Analysis Visualizations
Creates charts showing most in-demand skills
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Configuration
INPUT_FILE = 'data/processed/jobs_with_skills_summary.csv'
OUTPUT_DIR = 'outputs/visualizations'

# Dark theme configuration
DARK_THEME = {
    'plot_bgcolor': '#1e1e1e',
    'paper_bgcolor': '#2d2d2d',
    'font_color': '#e0e0e0',
    'gridcolor': '#404040'
}

def categorize_skills(df):
    """Separate skills into general skills vs specific software/tools"""
    
    software_tools = [
        'python', 'r', 'sql', 'sas', 'java', 'scala', 'javascript',
        'tableau', 'power bi', 'looker', 'qlik', 'excel', 'google sheets',
        'mongodb', 'oracle', 'snowflake', 'redshift', 'bigquery', 
        'mysql', 'postgresql', 'sql server',
        'aws', 'azure', 'gcp',
        'spark', 'hadoop', 'airflow', 'kafka', 'dbt', 'pandas', 'numpy',
        'git'
    ]
    
    general_skills = [
        'statistics', 'machine learning', 'regression', 'a/b testing',
        'business intelligence', 'data visualization', 'etl', 
        'data warehouse', 'data modeling', 'agile', 'api'
    ]
    
    df_software = df[df['skill'].isin(software_tools)].copy()
    df_general = df[df['skill'].isin(general_skills)].copy()
    
    return df_software, df_general


def create_skills_bar(df, title, filename, top_n=15):
    """Create horizontal bar chart for a specific skill category"""
    
    top_skills = df.head(top_n)
    
    fig = go.Figure(go.Bar(
        x=top_skills['percentage'],
        y=top_skills['skill'],
        orientation='h',
        marker=dict(
            color=top_skills['percentage'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(
                title=dict(text="% of Jobs", font=dict(color=DARK_THEME['font_color'])),
                tickfont=dict(color=DARK_THEME['font_color'])
            )
        ),
        text=top_skills['percentage'].apply(lambda x: f'{x:.1f}%'),
        textposition='outside',
        textfont=dict(color=DARK_THEME['font_color']),
        hovertemplate='<b>%{y}</b><br>%{x:.1f}% of jobs<br>%{customdata:,} postings',
        customdata=top_skills['job_count']
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Percentage of Job Postings',
        yaxis_title='',
        height=500,
        showlegend=False,
        plot_bgcolor=DARK_THEME['plot_bgcolor'],
        paper_bgcolor=DARK_THEME['paper_bgcolor'],
        font=dict(color=DARK_THEME['font_color']),
        xaxis=dict(gridcolor=DARK_THEME['gridcolor']),
        yaxis=dict(gridcolor=DARK_THEME['gridcolor'], categoryorder='total ascending', ticksuffix='  ')
    )
    
    fig.write_html(f'{OUTPUT_DIR}/{filename}')
    print(f"[OK] Saved: {OUTPUT_DIR}/{filename}")
    
    return fig


def create_top_skills_bar(df, top_n=20):
    """Create horizontal bar chart of top skills"""
    
    top_skills = df.head(top_n)
    
    fig = go.Figure(go.Bar(
        x=top_skills['percentage'],
        y=top_skills['skill'],
        orientation='h',
        marker=dict(
            color=top_skills['percentage'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(
                title=dict(text="% of Jobs", font=dict(color=DARK_THEME['font_color'])),
                tickfont=dict(color=DARK_THEME['font_color'])
            )
        ),
        text=top_skills['percentage'].apply(lambda x: f'{x:.1f}%'),
        textposition='outside',
        textfont=dict(color=DARK_THEME['font_color']),
        hovertemplate='<b>%{y}</b><br>%{x:.1f}% of jobs<br>%{customdata:,} postings',
        customdata=top_skills['job_count']
    ))
    
    fig.update_layout(
        title=f'Top {top_n} Most In-Demand Data Analyst Skills',
        xaxis_title='Percentage of Job Postings',
        yaxis_title='',
        height=600,
        showlegend=False,
        plot_bgcolor=DARK_THEME['plot_bgcolor'],
        paper_bgcolor=DARK_THEME['paper_bgcolor'],
        font=dict(color=DARK_THEME['font_color']),
        xaxis=dict(gridcolor=DARK_THEME['gridcolor']),
        yaxis=dict(gridcolor=DARK_THEME['gridcolor'], categoryorder='total ascending', ticksuffix='  ')
    )
    
    return fig


def create_skill_categories(df):
    """Group skills by category and compare"""
    
    # Define skill categories
    categories = {
        'Programming': ['python', 'r', 'sql', 'sas', 'java', 'scala'],
        'BI Tools': ['tableau', 'power bi', 'looker', 'qlik', 'excel'],
        'Cloud': ['aws', 'azure', 'gcp'],
        'Databases': ['mysql', 'postgresql', 'mongodb', 'oracle', 'snowflake', 
                      'redshift', 'bigquery', 'sql server'],
        'Big Data': ['spark', 'hadoop', 'kafka', 'airflow'],
        'Core Skills': ['statistics', 'machine learning', 'data visualization', 
                       'business intelligence', 'etl', 'data warehouse']
    }
    
    # Calculate category totals
    category_data = []
    for category, skills in categories.items():
        category_jobs = df[df['skill'].isin(skills)]['job_count'].sum()
        category_data.append({
            'category': category,
            'total_mentions': category_jobs
        })
    
    cat_df = pd.DataFrame(category_data).sort_values('total_mentions', ascending=True)
    
    fig = go.Figure(go.Bar(
        x=cat_df['total_mentions'],
        y=cat_df['category'],
        orientation='h',
        marker_color='#4CAF50',
        text=cat_df['total_mentions'].apply(lambda x: f'{x:,}'),
        textposition='outside',
        textfont=dict(color=DARK_THEME['font_color'])
    ))
    
    fig.update_layout(
        title='Skill Demand by Category',
        xaxis_title='Total Job Mentions',
        yaxis_title='',
        height=400,
        plot_bgcolor=DARK_THEME['plot_bgcolor'],
        paper_bgcolor=DARK_THEME['paper_bgcolor'],
        font=dict(color=DARK_THEME['font_color']),
        xaxis=dict(gridcolor=DARK_THEME['gridcolor']),
        yaxis=dict(gridcolor=DARK_THEME['gridcolor'], ticksuffix='  ')
    )
    
    return fig


def create_skills_treemap(df, top_n=30):
    """Create treemap showing skill proportions"""
    
    top_skills = df.head(top_n).copy()
    
    # Add a root for the treemap
    top_skills['all'] = 'All Skills'
    
    fig = px.treemap(
        top_skills,
        path=['all', 'skill'],
        values='job_count',
        title=f'Top {top_n} Skills Distribution',
        color='percentage',
        color_continuous_scale='Viridis',
        hover_data={'job_count': ':,', 'percentage': ':.1f'}
    )
    
    fig.update_layout(
        height=600,
        paper_bgcolor=DARK_THEME['paper_bgcolor'],
        font=dict(color=DARK_THEME['font_color'])
    )
    
    return fig


def main():
    """Run all visualizations"""
    
    print("="*70)
    print("SKILLS ANALYSIS: CREATING VISUALIZATIONS")
    print("="*70 + "\n")
    
    # Load data
    print(f"Loading skill summary from {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} unique skills\n")
    
    # Create visualizations
    print("Creating visualizations...")
    
    # Categorize skills
    df_software, df_general = categorize_skills(df)
    
    # 1. Top skills bar chart (all skills)
    fig1 = create_top_skills_bar(df, top_n=20)
    fig1.write_html(f'{OUTPUT_DIR}/top_skills_all.html')
    print(f"[OK] Saved: {OUTPUT_DIR}/top_skills_all.html")
    
    # 2. Software/Tools chart
    fig2 = create_skills_bar(df_software, 'Most In-Demand Software & Tools', 'top_software.html', top_n=15)
    
    # 3. General skills chart
    fig3 = create_skills_bar(df_general, 'Most In-Demand General Skills', 'top_general_skills.html', top_n=10)
    
    # 4. Category comparison
    fig4 = create_skill_categories(df)
    fig4.write_html(f'{OUTPUT_DIR}/skills_by_category.html')
    print(f"[OK] Saved: {OUTPUT_DIR}/skills_by_category.html")
    
    # 5. Treemap
    fig5 = create_skills_treemap(df, top_n=30)
    fig5.write_html(f'{OUTPUT_DIR}/skills_treemap.html')
    print(f"[OK] Saved: {OUTPUT_DIR}/skills_treemap.html")
    
    # Show in browser
    print("\nOpening visualizations...")
    fig2.show()  # Show software chart
    
    print("\n[DONE] All visualizations created!")
    print(f"Check {OUTPUT_DIR}/ for HTML files")


if __name__ == '__main__':
    main()

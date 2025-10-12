import pandas as pd
import plotly.graph_objects as go

print("Loading data...")
df = pd.read_csv('data/tableau/jobs_with_states.csv')

# Filter to sources with salary data
df_salary = df[df['source'].isin(['Google Search', 'Adzuna Oct 2025'])].copy()
df_salary = df_salary[df_salary['salary_min'].notna()]

print(f"Jobs with salary data: {len(df_salary):,}")

# Calculate average salary
df_salary['salary_avg'] = (df_salary['salary_min'] + df_salary['salary_max']) / 2

# Group by experience level and source
salary_by_exp_source = df_salary.groupby(['experience_level', 'source'])['salary_avg'].mean().reset_index()

print("\nAverage salaries:")
print(salary_by_exp_source)

# Prepare data for grouped bar chart
experience_order = ['Entry', 'Mid', 'Senior']

# Create separate traces for each source
fig = go.Figure()

for source in ['Google Search', 'Adzuna Oct 2025']:
    source_data = salary_by_exp_source[salary_by_exp_source['source'] == source]
    
    # Ensure all experience levels are present
    salaries = []
    for exp in experience_order:
        match = source_data[source_data['experience_level'] == exp]
        if len(match) > 0:
            salaries.append(match['salary_avg'].values[0])
        else:
            salaries.append(0)
    
    # Rename for cleaner legend

    display_name = 'Google Search (April 2025)' if source == 'Google Search' else 'Adzuna (October 2025)'
    fig.add_trace(go.Bar(
        name=display_name,
        x=experience_order,
        y=salaries,
        text=[f'${s:,.0f}' for s in salaries],
        textposition='outside'
    ))

# Update layout
fig.update_layout(
    title={
        'text': 'Average Data Analyst Salary by Experience Level<br><sub>Comparison of 2025 Data Sources</sub>',
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis_title='Experience Level',
    yaxis_title='Average Salary (USD)',
    barmode='group',
    yaxis=dict(
        tickformat='$,.0f',
        range=[0, max(salary_by_exp_source['salary_avg']) * 1.1]
    ),
    template='plotly_white',
    font=dict(size=12),
    height=500,
    width=800,
    showlegend=True,
    legend=dict(
    	title='Data Source',
    	orientation='v',  # Vertical
    	yanchor='top',
    	y=1,  # Top aligned with chart
    	xanchor='left',
  	x=1.02  # Just to the right of the chart

    )
)

# Save as HTML
output_file = 'visualizations/salary_by_experience.html'
print(f"\nSaving chart to {output_file}...")

import os
os.makedirs('visualizations', exist_ok=True)

fig.write_html(output_file)
print(f"Saved! Open {output_file} in your browser to view.")

# Also show in browser automatically
fig.show()

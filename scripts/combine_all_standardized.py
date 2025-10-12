import pandas as pd

print("Loading all datasets...")

# 1. Original Kaggle data (FIXED version with correct salaries)
df_original = pd.read_csv('data/tableau/jobs_enhanced_tableau_fixed.csv')
print(f"\n1. Original (Nov 2022 + April 2025): {len(df_original):,} jobs")
print(f"   Columns: {list(df_original.columns)}")
print(f"   Sources: {df_original['source'].unique()}")
print(f"   Work types: {df_original['work_type'].unique()}")
print(f"   Experience levels: {df_original['experience_level'].unique()}")

# 2. Indeed 2024
df_indeed = pd.read_csv('data/processed/indeed_2024_cleaned.csv')
print(f"\n2. Indeed 2024: {len(df_indeed):,} jobs")
print(f"   Work types: {df_indeed['work_type'].unique()}")
print(f"   Experience levels: {df_indeed['experience_level'].unique()}")

# 3. Adzuna Oct 2025
df_adzuna = pd.read_csv('data/processed/adzuna_cleaned.csv')
print(f"\n3. Adzuna Oct 2025: {len(df_adzuna):,} jobs")
print(f"   Work types: {df_adzuna['work_type'].unique()}")
print(f"   Experience levels: {df_adzuna['experience_level'].unique()}")

print("\n" + "="*50)
print("CHECKING STANDARDIZATION")
print("="*50)

# Check if all have required columns
required_cols = ['title', 'company_name', 'location', 'posted_date_clean', 
                 'salary_min', 'salary_max', 'work_type', 'experience_level', 'source']

for name, df in [("Original", df_original), ("Indeed", df_indeed), ("Adzuna", df_adzuna)]:
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        print(f"{name} missing columns: {missing}")
    else:
        print(f"{name}: All required columns present")

# Combine all
print("\n" + "="*50)
print("COMBINING ALL DATASETS")
print("="*50)

# Select common columns
common_cols = ['title', 'company_name', 'location', 'posted_date_clean',
               'salary_min', 'salary_max', 'work_type', 'experience_level', 
               'skills_text', 'software_text', 'source']

df_all = pd.concat([
    df_original[common_cols],
    df_indeed[common_cols],
    df_adzuna[common_cols]
], ignore_index=True)

# Add job_id
df_all.insert(0, 'job_id', range(1, len(df_all) + 1))

print(f"\nTotal jobs: {len(df_all):,}")

# Final summary
print("\n" + "="*50)
print("FINAL DATASET SUMMARY")
print("="*50)

print("\nBy source:")
print(df_all['source'].value_counts())

print("\nBy work type:")
print(df_all['work_type'].value_counts())

print("\nBy experience level:")
print(df_all['experience_level'].value_counts())

print("\nDate range:")
valid_dates = df_all['posted_date_clean'].dropna()
print(f"  {valid_dates.min()} to {valid_dates.max()}")

print("\nSalary data:")
has_salary = df_all['salary_min'].notna().sum()
print(f"  {has_salary:,} jobs ({has_salary/len(df_all)*100:.1f}%)")

# Save
print("\nSaving final complete dataset...")
df_all.to_csv('data/tableau/jobs_complete_standardized.csv', index=False)
print("Saved to: data/tableau/jobs_complete_standardized.csv")

print("\n" + "="*50)
print("READY FOR TABLEAU!")
print("="*50)

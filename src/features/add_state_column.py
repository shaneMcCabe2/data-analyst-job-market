import pandas as pd
import re
import ast

print("Loading data...")
df = pd.read_csv('data/tableau/jobs_complete_standardized.csv')

print(f"Total jobs: {len(df):,}")

# US state abbreviations for matching
US_STATES = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
    'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY',
    'District of Columbia': 'DC'
}

# Reverse mapping for abbreviation lookup
STATE_ABBREV = {abbrev: name for name, abbrev in US_STATES.items()}

def extract_state(location, source):
    """Extract state from location string"""
    
    if pd.isna(location):
        return None
    
    location_str = str(location)
    
    # Handle Remote/Anywhere
    if any(word in location_str.lower() for word in ['remote', 'anywhere']):
        return 'Remote'
    
    # For Adzuna - parse the dictionary structure
    if source == 'Adzuna Oct 2025' and '__CLASS__' in location_str:
        try:
            # Parse the dict string
            loc_dict = ast.literal_eval(location_str)
            area = loc_dict.get('area', [])
            
            # area format: ['US', 'State', 'County', 'City']
            if len(area) >= 2:
                state_name = area[1]  # Second element is state
                # Convert to abbreviation if full name
                return US_STATES.get(state_name, state_name)
        except:
            pass
    
    # Pattern 1: "City, ST" format (most common)
    match = re.search(r',\s*([A-Z]{2})(?:\s|$)', location_str)
    if match:
        abbrev = match.group(1)
        if abbrev in STATE_ABBREV:
            return abbrev
    
    # Pattern 2: "State, United States" format
    for state_name, abbrev in US_STATES.items():
        if state_name in location_str:
            return abbrev
    
    # Pattern 3: Full state name without comma
    location_upper = location_str.upper()
    for state_name, abbrev in US_STATES.items():
        if state_name.upper() in location_upper:
            return abbrev
    
    # Check for just state abbreviation
    for abbrev in STATE_ABBREV.keys():
        if abbrev in location_str.upper():
            return abbrev
    
    # If "United States" but no specific state
    if 'united states' in location_str.lower():
        return 'Unknown'
    
    return 'Unknown'

print("\nExtracting states from locations...")
df['state'] = df.apply(lambda row: extract_state(row['location'], row['source']), axis=1)

print("\nState distribution:")
state_counts = df['state'].value_counts()
print(state_counts.head(20))

print(f"\nRemote jobs: {(df['state'] == 'Remote').sum():,}")
print(f"Unknown location: {(df['state'] == 'Unknown').sum():,}")
print(f"Jobs with valid state: {(~df['state'].isin(['Remote', 'Unknown', None])).sum():,}")

# For salary map analysis - filter to jobs with both state and salary
df_mappable = df[(df['salary_min'].notna()) & 
                  (~df['state'].isin(['Remote', 'Unknown', None]))]

print(f"\nJobs mappable (have state AND salary): {len(df_mappable):,}")
print("\nTop 10 states with salary data:")
print(df_mappable['state'].value_counts().head(10))

# Save updated dataset
print("\nSaving with state column...")
df.to_csv('data/tableau/jobs_with_states.csv', index=False)
print("Saved to: data/tableau/jobs_with_states.csv")

print("\nReady for Tableau map visualization!")

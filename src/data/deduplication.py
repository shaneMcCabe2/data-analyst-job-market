import pandas as pd
from fuzzywuzzy import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

class JobDeduplicator:
    def __init__(self, similarity_threshold=0.85):
        self.similarity_threshold = similarity_threshold
    
    def normalize_company(self, company):
        """Normalize company names"""
        if pd.isna(company):
            return ""
        
        company = str(company).lower().strip()
        # Remove common suffixes
        company = re.sub(r'\b(inc|llc|ltd|corporation|corp|co|company)\b\.?', '', company)
        company = re.sub(r'\s+', ' ', company).strip()
        return company
    
    def normalize_title(self, title):
        """Normalize job titles"""
        if pd.isna(title):
            return ""
        
        title = str(title).lower().strip()
        # Remove Roman numerals and levels
        title = re.sub(r'\b(i{1,3}|iv|v|1|2|3)\b', '', title)
        # Remove common modifiers
        title = re.sub(r'\b(entry|senior|jr|sr|junior|mid|level)\b', '', title)
        title = re.sub(r'\s+', ' ', company).strip()
        return title
    
    def normalize_location(self, location):
        """Normalize location"""
        if pd.isna(location):
            return ""
        
        location = str(location).lower().strip()
        # Common city abbreviations
        replacements = {
            'new york city': 'new york',
            'nyc': 'new york',
            'sf': 'san francisco',
            'la': 'los angeles'
        }
        for old, new in replacements.items():
            location = location.replace(old, new)
        return location
    
    def find_duplicates(self, df):
        """Find duplicates using multiple methods"""
        
        print("Step 1: Normalizing fields...")
        df['company_norm'] = df['company_name'].apply(self.normalize_company)
        df['title_norm'] = df['title'].apply(self.normalize_title)
        df['location_norm'] = df['location'].apply(self.normalize_location)
        
        # Create composite key
        df['composite_key'] = (df['company_norm'] + '|' + 
                               df['title_norm'] + '|' + 
                               df['location_norm'])
        
        print("\nStep 2: Finding exact duplicates...")
        exact_dupes = df[df.duplicated(subset=['composite_key'], keep=False)]
        print(f"Found {len(exact_dupes):,} exact duplicate jobs")
        
        # Mark first occurrence to keep
        df['is_duplicate'] = df.duplicated(subset=['composite_key'], keep='first')
        df['duplicate_group'] = df.groupby('composite_key').ngroup()
        
        # Track which sources have duplicates
        duplicate_summary = df[df['is_duplicate']].groupby(['source', 'duplicate_group']).size()
        
        return df, duplicate_summary
    
    def text_similarity_check(self, df, sample_size=1000):
        """Check description similarity (expensive - run on sample)"""
        
        print("\nStep 3: Checking text similarity on sample...")
        
        # Sample non-duplicates for similarity check
        non_dupes = df[~df['is_duplicate']].sample(min(sample_size, len(df)))
        
        if 'description' not in df.columns or non_dupes['description'].isna().all():
            print("No descriptions available for similarity check")
            return df
        
        # Vectorize descriptions
        vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        descriptions = non_dupes['description'].fillna('').astype(str)
        
        try:
            tfidf_matrix = vectorizer.fit_transform(descriptions)
            
            # Calculate pairwise similarity
            similarity_matrix = cosine_similarity(tfidf_matrix)
            
            # Find pairs with high similarity
            similar_pairs = []
            for i in range(len(similarity_matrix)):
                for j in range(i + 1, len(similarity_matrix)):
                    if similarity_matrix[i][j] > self.similarity_threshold:
                        similar_pairs.append((i, j, similarity_matrix[i][j]))
            
            print(f"Found {len(similar_pairs)} potential text-based duplicates")
            
        except Exception as e:
            print(f"Error in similarity check: {e}")
        
        return df

# Usage
deduplicator = JobDeduplicator(similarity_threshold=0.85)
df_clean, duplicate_stats = deduplicator.find_duplicates(df)
df_clean = deduplicator.text_similarity_check(df_clean)

# Remove duplicates
df_final = df_clean[~df_clean['is_duplicate']]

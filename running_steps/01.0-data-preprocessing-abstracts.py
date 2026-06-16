import pandas as pd
from pathlib import Path  # Added missing import for Path handling
from nltk.corpus import stopwords
from src.preprocessing import (
    __general_preprocess__,
    __remove_plurals__,
    __remove_stopwords__,
    __get_word_freq__
)

# --- Configuration: Paths ---
input_file_path = "data/00-raw-data"
# Ensure the output directory exists
output_file_path = Path("data/02-processed-data")
output_file_path.mkdir(parents=True, exist_ok=True)

# --- Load Data ---
# Loading the raw CSV file
input_file = input_file_path/"epb_papers.csv"
full_df = pd.read_csv(input_file)

# --- Custom Stop Words Definition ---
# These lists filter out domain-specific noise (common academic terminology)
words_1k = ['urban', 'model', 'city', 'planning', 'study', 'data', 'spatial', 'use', 'area', 'based', 'paper', 'system']
words_other = ['result', 'ha', 'method', 'approach', 'using', 'different', 'new', 'used', 'level', 'research', 'two', 'information', 'wa', 'also', 'problem', 'effect', 'type', 'show', 'case', 'impact', 'within', 'however', 'developed', 'application', 'high', 'context', 'relationship', 'may', 'potential', 'characteristic', 'finding', 'term', 'well', 'value', 'first', 'present', 'number', 'large', 'distribution', "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "finding", "built"]
additional_words = ['provide', 'technique', 'important', 'various', 'existing', 'way', 'applied', 'understanding', 'significant', 'need', 'future', 'many', 'size', 'found', 'across', 'higher', 'function', 'identify', 'presented', 'time', 'issue', 'made', 'user', 'work', 'author', 'mean', 'map', 'article']

# Combine NLTK defaults with custom domain-specific stop words
regular_stop_words = stopwords.words('english')
epb_stop_words = list(set(regular_stop_words + words_1k + words_other + additional_words))

if __name__ == "__main__":
    # --- Preprocessing Pipeline ---
    # Create a backup of the raw abstract column
    full_df['abstract_raw'] = full_df['abstract'].astype(str)

    # Apply text cleaning sequence: general cleaning -> singularization -> stop-word removal
    full_df['abstract_clean'] = __general_preprocess__(full_df['abstract_raw'])
    full_df['abstract_clean'] = full_df['abstract_clean'].apply(__remove_plurals__)

    # Efficiency: Combine stop-word lists and run removal once
    full_df['abstract_clean'] = __remove_stopwords__(full_df['abstract_clean'], epb_stop_words)

    # --- Post-processing ---
    # Remove duplicate entries based on the cleaned abstract content
    full_df = full_df.drop_duplicates(subset=['abstract_clean'], keep='first')

    # Update 'abstract' column to contain the cleaned version for downstream modeling
    full_df['abstract'] = full_df['abstract_clean']

    # Generate word frequency statistics
    full_freq = __get_word_freq__(full_df['abstract'])

    # Select relevant columns for the final dataframe
    df = full_df[['title', 'authors', 'abstract', 'year']]

    # --- Export ---
    # Save the final processed file
    output_file = output_file_path/"epb_cleaned_abs.csv"
    full_df.to_csv(output_file, index=False)
    print(f"Process complete. File saved to: {output_file}")
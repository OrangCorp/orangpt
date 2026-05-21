import os
import pandas as pd
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

"""
script used to extract data relevant for our project from FAME-MT Dataset
https://github.com/laniqo-public/fame-mt
"""

def read_tsv_safe(file_path):
    """
    Safely read TSV files that might have inconsistent number of fields.
    Uses error handling to skip problematic lines.
    """
    try:
        # Try reading with error_bad_lines=False for older pandas
        # or on_bad_lines='skip' for newer pandas
        try:
            df = pd.read_csv(file_path, sep='\t', header=None, 
                           on_bad_lines='skip', engine='python',
                           names=['source', 'target'])
        except TypeError:
            # Fallback for older pandas versions
            df = pd.read_csv(file_path, sep='\t', header=None,
                           error_bad_lines=False, warn_bad_lines=False,
                           names=['source', 'target'])
        
        # Keep only rows with exactly 2 columns (source and target)
        df = df.dropna(subset=['source', 'target'])
        df = df[df['source'].notna() & df['target'].notna()]
        
        # Filter out rows where source or target might contain tabs (got split into multiple columns)
        # This is done by checking if there are no NaN values in unexpected columns
        return df[['source', 'target']]
    
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return pd.DataFrame(columns=['source', 'target'])

def extract_language_data(root_path, target_langs=['en', 'pl']):
    """
    Extract text data for specified languages from the dataset.
    
    Args:
        root_path: Path to the data directory
        target_langs: List of language codes to extract (default: ['en', 'pl'])
    """
    root_path = Path(root_path)
    dataset_path = root_path / 'dataset'
    neutral_path = root_path / 'neutral_samples_for_NMT_fine_tuning'
    
    # Initialize dictionaries to store data for each language
    lang_data = {lang: {'formal': [], 'informal': [], 'neutral': []} for lang in target_langs}
    
    # Track processed files to avoid duplicates
    processed_files = set()
    
    # Process formal/informal files
    print("Processing formal/informal files...")
    for lang_dir in dataset_path.iterdir():
        if not lang_dir.is_dir():
            continue
            
        dir_name = lang_dir.name  # e.g., 'all2de', 'all2pl', etc.
        target_lang = dir_name.replace('all2', '')  # Extract target language code
        
        print(f"  Processing directory: {dir_name}")
        
        for tsv_file in lang_dir.glob('*.tsv'):
            file_name = tsv_file.name
            
            # Skip if already processed
            if file_name in processed_files:
                continue
            processed_files.add(file_name)
            
            # Parse filename: e.g., 'en-de.formal.tsv' or 'pl-de.formal.tsv'
            if not '.' in file_name:
                continue
                
            parts = file_name.rsplit('.', 2)  # Split from right to handle potential dots in names
            if len(parts) < 3:
                continue
                
            lang_pair = parts[0]  # e.g., 'en-de' or 'pl-de'
            formality = parts[1]  # 'formal' or 'informal'
            
            if '-' not in lang_pair:
                continue
                
            source_lang = lang_pair.split('-')[0]  # Source language
            
            # Read the TSV file
            df = read_tsv_safe(tsv_file)
            
            if len(df) == 0:
                continue
            
            # Extract data for target languages (both as source and target)
            for lang in target_langs:
                # If this language is the source language, extract source column
                if source_lang == lang:
                    if formality in ['formal', 'informal']:
                        sentences = df['source'].dropna().tolist()
                        lang_data[lang][formality].extend(sentences)
                        print(f"    Added {len(sentences)} sentences from source of {file_name}")
                
                # If this language is the target language, extract target column
                if target_lang == lang:
                    if formality in ['formal', 'informal']:
                        sentences = df['target'].dropna().tolist()
                        lang_data[lang][formality].extend(sentences)
                        print(f"    Added {len(sentences)} sentences from target of {file_name}")
    
    # Process neutral samples if the directory exists
    if neutral_path.exists():
        print("\nProcessing neutral files...")
        for tsv_file in neutral_path.glob('*.tsv'):
            file_name = tsv_file.name
            print(f"  Processing: {file_name}")
            
            # Parse filename to determine languages
            # Format: e.g., 'en-pl.neutral.tsv' or 'sv-pl.neutral.tsv'
            if not '.' in file_name:
                continue
                
            parts = file_name.rsplit('.', 2)
            if len(parts) < 3:
                continue
                
            lang_pair = parts[0]  # e.g., 'en-pl' or 'sv-pl'
            
            if '-' not in lang_pair:
                continue
                
            source_lang = lang_pair.split('-')[0]
            target_lang = lang_pair.split('-')[1]
            
            # Only process if at least one of our target languages is involved
            relevant_langs = [lang for lang in target_langs if lang in [source_lang, target_lang]]
            
            if not relevant_langs:
                continue
            
            # Read the TSV file
            df = read_tsv_safe(tsv_file)
            
            if len(df) == 0:
                continue
            
            # Extract neutral sentences for relevant languages
            for lang in relevant_langs:
                if source_lang == lang:
                    sentences = df['source'].dropna().tolist()
                    lang_data[lang]['neutral'].extend(sentences)
                    print(f"    Added {len(sentences)} neutral sentences for {lang}")
                
                if target_lang == lang:
                    sentences = df['target'].dropna().tolist()
                    lang_data[lang]['neutral'].extend(sentences)
                    print(f"    Added {len(sentences)} neutral sentences for {lang}")
    
    # Remove duplicates while preserving order
    for lang in target_langs:
        for formality_level in ['formal', 'informal', 'neutral']:
            if lang_data[lang][formality_level]:
                # Remove duplicates
                seen = set()
                unique_sentences = []
                for sentence in lang_data[lang][formality_level]:
                    if sentence not in seen:
                        seen.add(sentence)
                        unique_sentences.append(sentence)
                lang_data[lang][formality_level] = unique_sentences
                
    return lang_data

def save_to_csv(lang_data, output_path, target_langs=['en', 'pl']):
    """
    Save extracted data to separate compressed CSV files for each formality level.
    
    Args:
        lang_data: Dictionary containing extracted data
        output_path: Path where CSV files will be saved
        target_langs: List of language codes
    """
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    
    for lang in target_langs:
        if lang not in lang_data:
            continue
        
        # Save formal data
        if lang_data[lang]['formal']:
            formal_df = pd.DataFrame({
                'text': lang_data[lang]['formal'],
                'formality': '1'
            })
            output_file = output_path / f"{lang}_formal.csv.gz"
            formal_df.to_csv(output_file, index=False, compression='gzip')
            print(f"Saved {len(formal_df)} formal records to {output_file}")
        
        # Save informal data
        if lang_data[lang]['informal']:
            informal_df = pd.DataFrame({
                'text': lang_data[lang]['informal'],
                'formality': '-1'
            })
            output_file = output_path / f"{lang}_informal.csv.gz"
            informal_df.to_csv(output_file, index=False, compression='gzip')
            print(f"Saved {len(informal_df)} informal records to {output_file}")
        
        # Save neutral data
        if lang_data[lang]['neutral']:
            neutral_df = pd.DataFrame({
                'text': lang_data[lang]['neutral'],
                'formality': '0'
            })
            output_file = output_path / f"{lang}_neutral.csv.gz"
            neutral_df.to_csv(output_file, index=False, compression='gzip')
            print(f"Saved {len(neutral_df)} neutral records to {output_file}")
        
        if not any([lang_data[lang]['formal'], lang_data[lang]['informal'], lang_data[lang]['neutral']]):
            print(f"No data found for {lang}")

def main():
    # Set your paths here
    root_path = r"C:\dadada4\orangpt\data"
    output_path = r"C:\dadada4\orangpt\extracted_data"
    
    print(f"Processing dataset from: {root_path}")
    print("=" * 60)
    
    # Extract data for Polish and English
    target_languages = ['en', 'pl']
    lang_data = extract_language_data(root_path, target_languages)
    
    print("\n" + "=" * 60)
    print("Saving results...")
    
    # Save to CSV files
    save_to_csv(lang_data, output_path, target_languages)
    
    print("\n" + "=" * 60)
    print("Extraction complete!")
    
    # Print summary statistics
    for lang in target_languages:
        if lang in lang_data:
            total_formal = len(lang_data[lang]['formal'])
            total_informal = len(lang_data[lang]['informal'])
            total_neutral = len(lang_data[lang]['neutral'])
            print(f"\n{lang.upper()} statistics:")
            print(f"  - Formal sentences: {total_formal}")
            print(f"  - Informal sentences: {total_informal}")
            print(f"  - Neutral sentences: {total_neutral}")
            print(f"  - Total: {total_formal + total_informal + total_neutral}")

if __name__ == "__main__":
    main()
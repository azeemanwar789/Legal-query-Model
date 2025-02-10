import nltk
nltk.download('stopwords')
nltk.download('punkt')
import csv
import re
import spacy
from nltk.corpus import stopwords

# Load SpaCy model for NLP tasks (ensure 'en_core_web_sm' is installed)
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    import spacy.cli
    spacy.cli.download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')

# Function to read the structured dataset from CSV
def read_structured_csv(input_csv_path):
    structured_data = []
    with open(input_csv_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            structured_data.append(row)
    return structured_data

# Function to normalize text (e.g., uniform capitalization, phrasing)
def normalize_text(text):
    if not text:
        return ''
    # Convert to lowercase
    text = text.lower()
    # Replace variations of terms with standardized terms
    text = re.sub(r'\b(life imprisonment|life sentence)\b', 'life imprisonment', text)
    return text

# Function to extract keywords using SpaCy
def extract_keywords(text):
    if not text:
        return []

    doc = nlp(text)
    stop_words = set(stopwords.words('english'))
    keywords = [
        token.text for token in doc
        if token.pos_ in ['NOUN', 'PROPN', 'VERB'] and token.text.lower() not in stop_words
    ]
    return keywords

# Function to refine the structured dataset
def refine_dataset(structured_data):
    refined_data = []
    
    for row in structured_data:
        try:
            # Normalize text for each column
            row['Offense'] = normalize_text(row.get('Offense', ''))
            row['Punishment'] = normalize_text(row.get('Punishment', ''))
            row['Definition'] = normalize_text(row.get('Definition', ''))
            row['Illustration'] = normalize_text(row.get('Illustration', ''))

            # Extract keywords for specific columns
            row['Offense Keywords'] = ', '.join(extract_keywords(row['Offense']))
            row['Punishment Keywords'] = ', '.join(extract_keywords(row['Punishment']))
            row['Exceptions Keywords'] = ', '.join(extract_keywords(row.get('Exceptions', '')))
            row['Illustration Keywords'] = ', '.join(extract_keywords(row['Illustration']))

            refined_data.append(row)
        except Exception as e:
            row['Error'] = str(e)
            refined_data.append(row)

    return refined_data

# Function to save the refined dataset to a new CSV
def save_refined_data_to_csv(refined_data, output_csv_path):
    # Dynamically extract all fieldnames from the refined data
    fieldnames = set()
    for row in refined_data:
        fieldnames.update(row.keys())
    fieldnames = list(fieldnames)  # Convert to list for CSV writer

    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(refined_data)

# Main execution
structured_data_path = r"C:\Azeem's Work\IDC Internship\2nd Month\Report-Tasks\Week 9 to 12 Material\Extracted text\New_try\annotations\annotated_data2.csv"  # Input dataset
output_csv_path = r"C:\Azeem's Work\IDC Internship\2nd Month\Report-Tasks\Week 9 to 12 Material\Extracted text\Parsed text\Refined data output folder\refined_dataset2.csv"  # Output refined dataset

# Read the structured dataset from CSV
structured_data = read_structured_csv(structured_data_path)

# Refine the dataset (normalize and extract keywords)
refined_data = refine_dataset(structured_data)

# Save the refined dataset to a new CSV
save_refined_data_to_csv(refined_data, output_csv_path)

print(f"Refined dataset saved to {output_csv_path}")

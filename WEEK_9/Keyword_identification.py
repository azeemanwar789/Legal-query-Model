import csv
import re
import spacy
from nltk.corpus import stopwords
import nltk

# Ensure required resources are downloaded
nltk.download('stopwords')
nltk.download('punkt')

# Load SpaCy language model
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    import spacy.cli
    spacy.cli.download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')

# Function to normalize text
def normalize_text(text):
    if not text:
        return ""
    # Convert to lowercase
    text = text.lower()
    # Standardize specific terms
    text = re.sub(r'\b(life imprisonment|life sentence)\b', 'life imprisonment', text)
    return text

# Function to extract keywords
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

# Function to refine the dataset
def refine_dataset(data):
    refined_data = []
    for row in data:
        try:
            # Normalize text columns
            row['Offense'] = normalize_text(row.get('Offense', ''))
            row['Punishment'] = normalize_text(row.get('Punishment', ''))
            row['Exceptions'] = normalize_text(row.get('Exceptions', ''))
            row['Illustration'] = normalize_text(row.get('Illustration', ''))

            # Extract keywords for each column
            row['Offense Keywords'] = ', '.join(extract_keywords(row['Offense']))
            row['Punishment Keywords'] = ', '.join(extract_keywords(row['Punishment']))
            row['Exceptions Keywords'] = ', '.join(extract_keywords(row['Exceptions']))
            row['Illustration Keywords'] = ', '.join(extract_keywords(row['Illustration']))

            refined_data.append(row)
        except Exception as e:
            row['Error'] = str(e)
            refined_data.append(row)
    return refined_data

# Function to save refined data to CSV
def save_refined_data_to_csv(refined_data, output_csv_path):
    # Extract all fieldnames dynamically
    fieldnames = set()
    for row in refined_data:
        fieldnames.update(row.keys())
    fieldnames = list(fieldnames)

    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(refined_data)

# Main execution
if __name__ == "__main__":
    input_csv_path = r"C:\Azeem's Work\IDC Internship\2nd Month\Report-Tasks\Week 9 to 12 Material\Extracted text\Parsed text\Refined data output folder\refined_dataset2.csv"  # Replace with your input file path
    output_csv_path = r"C:\Azeem's Work\IDC Internship\2nd Month\Report-Tasks\Week 9 to 12 Material\Extracted text\Parsed text\Keyword identification and dataset refinement\morerefined_data2.csv"  # Replace with your output file path

    # Read structured dataset
    structured_data = []
    with open(input_csv_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            structured_data.append(row)

    # Refine the dataset
    refined_data = refine_dataset(structured_data)

    # Save the refined dataset
    save_refined_data_to_csv(refined_data, output_csv_path)

    print(f"Refined dataset saved to {output_csv_path}")

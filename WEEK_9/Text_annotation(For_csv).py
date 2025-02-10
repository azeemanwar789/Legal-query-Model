import csv
import json
import spacy
from nltk.corpus import stopwords
import nltk

# Ensure required resources are downloaded
nltk.download('stopwords')

# Load SpaCy language model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Define stopwords
stop_words = set(stopwords.words("english"))

# Function to normalize text
def normalize_text(text):
    if not text:
        return ""
    text = text.lower().strip()  # Convert to lowercase and strip whitespace
    text = text.replace("life sentence", "life imprisonment")
    text = text.replace("death sentence", "capital punishment")
    return text

# Function to extract keywords
def extract_keywords(text):
    if not text:
        return []
    doc = nlp(text)
    keywords = [
        token.text for token in doc 
        if token.pos_ in ["NOUN", "PROPN", "VERB"] and token.text.lower() not in stop_words
    ]
    return keywords

# Prepare data for annotation
def prepare_annotation_data(input_csv_path):
    annotation_data = []
    with open(input_csv_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                # Normalize and extract keywords
                normalized_offense = normalize_text(row.get("Offense", ""))
                normalized_punishment = normalize_text(row.get("Punishment", ""))
                normalized_exception = normalize_text(row.get("Exceptions", ""))
                normalized_example = normalize_text(row.get("Illustration", ""))

                offense_keywords = extract_keywords(normalized_offense)
                punishment_keywords = extract_keywords(normalized_punishment)
                exception_keywords = extract_keywords(normalized_exception)
                example_keywords = extract_keywords(normalized_example)

                # Create annotation data
                annotation_data.append({
                    "id": row.get("Section", "N/A"),
                    "Offense": row.get("Offense", ""),
                    "Punishment": row.get("Punishment", ""),
                    "Exceptions": row.get("Exceptions", ""),
                    "Illustration": row.get("Illustration", ""),
                    "Offense_Keywords": ", ".join(offense_keywords),
                    "Punishment_Keywords": ", ".join(punishment_keywords),
                    "Exceptions_Keywords": ", ".join(exception_keywords),
                    "Illustration_Keywords": ", ".join(example_keywords),
                })
            except Exception as e:
                print(f"Error processing row: {row}. Exception: {e}")
    return annotation_data

# Save annotation data to CSV
def save_to_csv(annotation_data, output_path):
    with open(output_path, "w", newline='', encoding="utf-8") as file:
        fieldnames = ["id", "Offense", "Punishment", "Exceptions", "Illustration",
                      "Offense_Keywords", "Punishment_Keywords", "Exceptions_Keywords", "Illustration_Keywords"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        for item in annotation_data:
            writer.writerow(item)

# Specify file paths
input_csv_path = r"C:\Azeem's Work\IDC Internship\2nd Month\Report-Tasks\Week 9 to 12 Material\Extracted text\Parsed text\Keyword identification and dataset refinement\morerefined_data2.csv"  # Replace with the path to your input CSV file
output_csv_path = r"C:\Azeem's Work\IDC Internship\2nd Month\Report-Tasks\Week 9 to 12 Material\Extracted text\Parsed text\Keyword identification and dataset refinement\Text_annotations\annotation_data2.csv"  # Path for the output CSV file

# Prepare data for annotation
annotation_data = prepare_annotation_data(input_csv_path)

# Save prepared data to a CSV file
save_to_csv(annotation_data, output_csv_path)

print(f"Annotation data saved to {output_csv_path}")

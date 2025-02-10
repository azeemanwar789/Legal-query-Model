import csv
import re

# Function to read structured CSV file
def read_structured_csv(input_csv_path):
    structured_data = []
    with open(input_csv_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            structured_data.append(row)
    return structured_data

# Function to annotate exceptions and dependencies
def annotate_exceptions_and_dependencies(structured_data):
    for row in structured_data:
        # Annotate dependencies: Check if current section refers to a previous section
        section_number = row['Section']
        if section_number:
            # Check if the section contains dependencies (e.g., "See Section X" or "refer to Section X")
            dependencies = re.findall(r"section\s+(\d+)", row['Offense'])
            row['Dependencies'] = ', '.join(dependencies) if dependencies else ''

        # Annotate exceptions: Look for keywords such as "except", "unless", "provided that"
        exceptions = re.findall(r"(except|unless|provided that|provided)", row['Offense'], re.IGNORECASE)
        row['Exceptions'] = ', '.join(exceptions) if exceptions else ''

        # Add keywords for search: Look for specific terms like "self-defense", "culpable homicide"
        keywords = []
        if 'self-defense' in row['Offense'].lower():
            keywords.append('self-defense')
        if 'culpable homicide' in row['Offense'].lower():
            keywords.append('culpable homicide')

        row['Keywords'] = ', '.join(keywords) if keywords else ''

    return structured_data

# Function to save annotated data to a new CSV
def save_annotated_data_to_csv(annotated_data, output_csv_path):
    keys = ['Section', 'Clause', 'Offense', 'Punishment', 'Definition', 'Illustration', 'Dependencies', 'Exceptions', 'Keywords']
    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(annotated_data)

# Main execution
structured_data_path = r"C:\Azeem's Work\IDC Internship\2nd Month\Report-Tasks\Week 9 to 12 Material\Extracted text\New_try\structured_data2.csv"  # Input structured CSV file
output_csv_path = r"C:\Azeem's Work\IDC Internship\2nd Month\Report-Tasks\Week 9 to 12 Material\Extracted text\New_try\annotations\annotated_data2.csv"  # Output CSV file

# Read the structured CSV data
structured_data = read_structured_csv(structured_data_path)

# Annotate exceptions and dependencies, and add keywords for search
annotated_data = annotate_exceptions_and_dependencies(structured_data)

# Save the annotated data to a new CSV
save_annotated_data_to_csv(annotated_data, output_csv_path)

print(f"Annotated data saved to {output_csv_path}")

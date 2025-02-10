import pdfplumber
import csv
import re

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to structure the data into sections, clauses, illustrations, etc.
def structure_data(text):
    data = []
    
    # Regular expressions for detecting section, clause, and keywords
    section_regex = r"section\s+(\d+)"
    clause_regex = r"clause\s+[a-zA-Z\(\)0-9]+"
    illustration_heading_regex = r"illustration"
    punishment_heading_regex = r"punishment"
    definition_heading_regex = r"definition"

    # Split the document into lines to analyze the structure
    lines = text.split('\n')

    current_section = None
    current_clause = None
    illustration_text = []
    punishment_text = []
    definition_text = []
    in_illustration_block = False
    in_punishment_block = False
    in_definition_block = False

    for line in lines:
        # Check for section number
        section_match = re.search(section_regex, line, re.IGNORECASE)
        if section_match:
            # Save any ongoing data (illustration, punishment, or definition)
            if illustration_text or punishment_text or definition_text:
                data.append({
                    'Section': current_section,
                    'Clause': current_clause if current_clause else '',
                    'Offense': '',
                    'Punishment': ' '.join(punishment_text),
                    'Definition': ' '.join(definition_text),
                    'Illustration': ' '.join(illustration_text)
                })
                illustration_text = []  # Reset illustration data
                punishment_text = []    # Reset punishment data
                definition_text = []    # Reset definition data
            
            # Update current section
            current_section = section_match.group(0)
            current_clause = None  # Reset clause for new section
            
            # Add a new row for the section
            data.append({
                'Section': current_section,
                'Clause': '',
                'Offense': '',
                'Punishment': '',
                'Definition': '',
                'Illustration': ''
            })
            in_illustration_block = False  # Reset illustration block status
            in_punishment_block = False    # Reset punishment block status
            in_definition_block = False    # Reset definition block status
            continue

        # Check for clause
        clause_match = re.search(clause_regex, line, re.IGNORECASE)
        if clause_match:
            current_clause = line.strip()  # Store the full line containing the clause keyword
            # Add a row for the clause
            data.append({
                'Section': current_section if current_section else '',
                'Clause': current_clause,
                'Offense': '',
                'Punishment': '',
                'Definition': '',
                'Illustration': ''
            })
            continue

        # Check for illustration heading
        if re.search(illustration_heading_regex, line, re.IGNORECASE):
            in_illustration_block = True  # Start recording illustration text
            in_punishment_block = False
            in_definition_block = False
            continue
        
        # Check for punishment heading
        if re.search(punishment_heading_regex, line, re.IGNORECASE):
            in_punishment_block = True  # Start recording punishment text
            in_illustration_block = False
            in_definition_block = False
            continue

        # Check for definition heading
        if re.search(definition_heading_regex, line, re.IGNORECASE):
            in_definition_block = True  # Start recording definition text
            in_illustration_block = False
            in_punishment_block = False
            continue
        
        # Collect illustration text if inside an illustration block
        if in_illustration_block:
            if line.strip():  # Add non-empty lines
                illustration_text.append(line.strip())
            else:
                # End of illustration block if an empty line is encountered
                in_illustration_block = False

        # Collect punishment text if inside a punishment block
        if in_punishment_block:
            if line.strip():  # Add non-empty lines
                punishment_text.append(line.strip())
            else:
                # End of punishment block if an empty line is encountered
                in_punishment_block = False

        # Collect definition text if inside a definition block
        if in_definition_block:
            if line.strip():  # Add non-empty lines
                definition_text.append(line.strip())
            else:
                # End of definition block if an empty line is encountered
                in_definition_block = False

        # Handle offenses (e.g., containing "accused")
        if 'accused' in line.lower() and current_section:
            data[-1]['Offense'] = line.strip()

    # Handle any remaining data at the end of the document
    if illustration_text or punishment_text or definition_text:
        data.append({
            'Section': current_section,
            'Clause': current_clause if current_clause else '',
            'Offense': '',
            'Punishment': ' '.join(punishment_text),
            'Definition': ' '.join(definition_text),
            'Illustration': ' '.join(illustration_text)
        })

    return data

# Function to save the structured data into a CSV file
def save_to_csv(data, output_csv_path):
    keys = ['Section', 'Clause', 'Offense', 'Punishment', 'Definition', 'Illustration']
    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

# Main execution
pdf_path = r"C:\Azeem's Work\IDC Internship\2nd Month\Report-Tasks\Week 9 to 12 Material\Dataset 2  legal Solution.pdf"  # Replace with the path to your PDF
output_csv_path = r"C:\Azeem's Work\IDC Internship\2nd Month\Report-Tasks\Week 9 to 12 Material\Extracted text\New_try\structured_data2.csv"  # Output CSV file

# Extract text from the PDF
text = extract_text_from_pdf(pdf_path)

# Structure the data
structured_data = structure_data(text)

# Save to CSV
save_to_csv(structured_data, output_csv_path)

print(f"Data extracted and saved to {output_csv_path}")

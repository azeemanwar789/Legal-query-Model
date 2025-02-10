import re
import json
import os

# Function to extract legal text based on clauses, sections, and explanations from a JSON file
def extract_legal_text_and_structure_from_json(input_json_file, output_folder):
    try:
        # Read the JSON file containing legal text
        with open(input_json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Assuming that the JSON is a list of objects and each object contains the "Content" field
        if isinstance(data, list):
            text = " ".join([item.get("Content", "") for item in data])
        else:
            text = data.get("Content", "")

        # Define keywords to match for Sections, Clauses, Explanations, and Illustrations
        section_pattern = r"(Section\s+\d+|Clause\s+\d+|Chapter\s+\w+)"
        explanation_pattern = r"Explanation\s*[\.\-]?\s*(.*?)(?=\n|$)"
        illustration_pattern = r"Illustration\s*[\.\-]?\s*(.*?)(?=\n|$)"
        
        # Split content into sections based on headings
        sections = re.split(section_pattern, text)

        structured_data = []
        current_section = None
        
        # Iterate through sections
        for section in sections:
            # Check if this is a Section or Clause using regex
            match = re.search(section_pattern, section)
            
            if match:
                # If a Section/Clause is found, finalize the current section if it exists
                if current_section is not None:
                    structured_data.append(current_section)
                
                # Start a new section
                current_section = {"Section/Clause": match.group().strip(), "Content": ""}
            
            # If current_section is None, skip this iteration to avoid adding content without a header
            if current_section is None:
                continue
            
            # Add content for the current section
            current_section["Content"] += section.strip()

            # Extract Explanations and Illustrations
            explanations = re.findall(explanation_pattern, section)
            illustrations = re.findall(illustration_pattern, section)

            # Store explanations and illustrations if found
            if explanations:
                current_section["Explanations"] = explanations
            if illustrations:
                current_section["Illustrations"] = illustrations
        
        # Append the last section if it exists
        if current_section is not None:
            structured_data.append(current_section)

        # Write the structured data to a JSON file
        output_file_path = os.path.join(output_folder, "structured_legal_data.json")
        with open(output_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(structured_data, json_file, indent=4, ensure_ascii=False)

        print(f"Structured data saved at: {output_file_path}")
        return output_file_path

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

input_json_file = r"C:\Azeem's Work\IDC Internship\2nd Month\Report-Tasks\Week 9 to 12 Material\Extracted text\Dataset 2  legal Solution_output.json"
output_folder = r"C:\Azeem's Work\IDC Internship\2nd Month\Report-Tasks\Week 9 to 12 Material\Extracted text\Parsed text\Dataset 2 legal Solution(Parsed)"

# Make sure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Call the function to extract and structure legal text from the input JSON
output_file = extract_legal_text_and_structure_from_json(input_json_file, output_folder)
if output_file:
    print(f"Output saved at: {output_file}")

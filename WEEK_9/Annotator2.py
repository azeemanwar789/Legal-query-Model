import json
import re
import os

def annotate_json(input_path, output_path, keyword_map):
    """
    Annotates a JSON file by linking specific clauses to general sections
    and adding keywords for improved search.

    Parameters:
    input_path (str): Path to the input JSON file.
    output_path (str): Path to save the annotated JSON file.
    keyword_map (dict): A dictionary mapping sections to keywords.
    """
    try:
        # Check if input file exists
        if not os.path.exists(input_path):
            print(f"Error: Input file '{input_path}' does not exist.")
            return
        
        # Load JSON data
        with open(input_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        # Validate JSON format
        if not isinstance(data, list):
            print("Error: JSON must be a list of objects (dictionaries).")
            return

        # Annotate each entry in the JSON
        for entry in data:
            # Extract section number if available
            section = entry.get("section")
            if not section:
                continue

            # Link exceptions or dependencies (e.g., "See Section 100")
            description = entry.get("description", "")
            referenced_sections = re.findall(r"Section (\d+)", description)
            entry["references"] = referenced_sections

            # Add keywords for search based on the section number
            if section in keyword_map:
                entry["keywords"] = keyword_map[section]
            else:
                entry["keywords"] = []

        # Save the annotated JSON to the output file
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(output_path, 'w', encoding='utf-8') as output_file:
            json.dump(data, output_file, ensure_ascii=False, indent=4)
        
        print(f"Annotated JSON successfully saved to '{output_path}'")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_file = r"C:\Azeem's Work\IDC Internship\2nd Month\Report-Tasks\Week 9 to 12 Material\Extracted text\Parsed text\Dataset legal Solution(Parsed)\structured_legal_data(Dataset2).json"
output_file = r"C:\Azeem's Work\IDC Internship\2nd Month\Report-Tasks\Week 9 to 12 Material\Extracted text\Parsed text\Annotated files\annotated_legal_data2.json"

# Map of keywords for specific sections
keyword_map = {
    "35": ["general exceptions", "criminal liability", "intentional acts"],
    "100": ["self-defense", "culpable homicide", "justified killing"],
    "299": ["culpable homicide", "criminal act", "intention"],
    "300": ["murder", "intention", "premeditation"],
    "304": ["culpable homicide not amounting to murder", "exceptions", "penalty"]
}

annotate_json(input_file, output_file, keyword_map)

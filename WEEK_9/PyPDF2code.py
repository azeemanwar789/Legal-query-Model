import PyPDF2
import os
import json

def extract_text_pypdf2(file_path, output_folder):
    try:
        with open(file_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            extracted_text = []
            
            # Extract text page by page
            for page_number, page in enumerate(reader.pages, start=1):
                text = page.extract_text()
                extracted_text.append({"Page": page_number, "Content": text.strip()})
            
            # Create JSON output file path
            file_name = os.path.basename(file_path).replace('.pdf', '_output.json')
            output_file_path = os.path.join(output_folder, file_name)
            
            # Save the extracted text as JSON
            with open(output_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(extracted_text, json_file, indent=4, ensure_ascii=False)

            print(f"Text extracted and saved to: {output_file_path}")
            return output_file_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

file_path = r"C:\Azeem's Work\IDC Internship\2nd Month\Report-Tasks\Week 9 to 12 Material\Dataset 1  legal Solution.pdf"
output_folder = r"C:\Azeem's Work\IDC Internship\2nd Month\Report-Tasks\Week 9 to 12 Material\Extracted text"

# Make sure the output folder exists
os.makedirs(output_folder, exist_ok=True)

output_file = extract_text_pypdf2(file_path, output_folder)
if output_file:
    print(f"Output saved at: {output_file}")

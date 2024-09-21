# docling_integration.py - Version 1.0

import os
import pandas as pd
import requests
import uuid
import time
from docling.extractor import Extractor
from docling.translator import Translator  # Assuming Docling has a translation feature; if not, use the Azure Translator API.

# Azure Translator settings
key = "20069e8c4ccd4f3d820752c43f7b0544"
endpoint = "https://api.cognitive.microsofttranslator.com"
location = "southeastasia"

def translate_text(text):
    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': 'ms',
        'to': 'en'
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': text}]

    try:
        request = requests.post(constructed_url, params=params, headers=headers, json=body)
        response = request.json()
        return response[0]['translations'][0]['text']
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return ""

# Set the directory where uploaded PDFs are stored
pdf_folder = os.getcwd()  # Modify as needed

all_data = []

# Process all PDF files in the folder using Docling
for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)
        print(f"Processing: {filename}")

        # Use Docling's Extractor to get the content
        try:
            extractor = Extractor(pdf_path)
            extracted_content = extractor.extract()  # This method should provide structured content
            
            for page, content in extracted_content.items():  # Assuming 'extract' returns a dictionary
                sentences = content.split('.')
                for sentence in sentences:
                    translated = translate_text(sentence.strip())
                    all_data.append({
                        "Filename": filename,
                        "Malay": sentence,
                        "English": translated,
                        "Page": page,
                        "Type": "text"
                    })
                    time.sleep(0.1)  # To avoid hitting rate limits
                    
        except Exception as e:
            print(f"Error processing {pdf_path} with Docling: {str(e)}")

# Create a DataFrame
df = pd.DataFrame(all_data)

# Save the DataFrame to Excel
output_file = os.path.join(pdf_folder, "all_newsletters_content_translated_docling.xlsx")
df.to_excel(output_file, index=False)

print(f"Processing complete. Data saved to {output_file}")

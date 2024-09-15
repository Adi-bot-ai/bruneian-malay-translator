# batch_pdf_extractor_translator.py - Version 4.0

import os
import PyPDF2
import pandas as pd
import re
import requests
import uuid
import time

# Azure Translator settings
key = "20069e8c4ccd4f3d820752c43f7b0544"
endpoint = "https://api.cognitive.microsofttranslator.com"
location = "southeastasia"

def extract_text_from_pdf(pdf_path):
    text_content = []
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                if text:
                    text_content.append({"page": page_num, "content": text})
    except Exception as e:
        print(f"Error processing {pdf_path}: {str(e)}")
    return text_content

def simple_sentence_split(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

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

    body = [{
        'text': text
    }]

    try:
        request = requests.post(constructed_url, params=params, headers=headers, json=body)
        response = request.json()
        return response[0]['translations'][0]['text']
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return ""

# Use the current working directory
pdf_folder = os.getcwd()

all_data = []

# Process all PDF files in the folder
for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)
        print(f"Processing: {filename}")
        
        extracted_content = extract_text_from_pdf(pdf_path)
        
        for item in extracted_content:
            sentences = simple_sentence_split(item['content'])
            for sentence in sentences:
                translated = translate_text(sentence)
                all_data.append({
                    "Filename": filename,
                    "Malay": sentence,
                    "English": translated,
                    "Page": item['page'],
                    "Type": "text"
                })
                time.sleep(0.1)  # To avoid hitting rate limits

# Create DataFrame
df = pd.DataFrame(all_data)

# Save to Excel
output_file = os.path.join(pdf_folder, "all_newsletters_content_translated.xlsx")
df.to_excel(output_file, index=False)

print(f"Processing complete. Data saved to {output_file}")
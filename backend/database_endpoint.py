import os
import requests
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from huggingface_hub import HfApi, hf_hub_download, HfFolder
import csv
from io import StringIO
import sys 
import re 
import pickle


load_dotenv('.env')

app = Flask(__name__)

repo_id = 'asaurasieu/debatebot'
repo_url = 'https://huggingface.co/asaurasieu/debatebot'
hf_read_token = os.getenv('HF_READ_TOKEN')

def list_hf_repository_files(repo_url):
    """List all files in a specified Hugging Face repository's URL."""
    print(f'Fetching repository URL: {repo_url}')
    response = requests.get(repo_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    available_docs = [a['href'] for a in soup.find_all('a', {'class': 'Link--active'})]
    print(f'Found {len(available_docs)} available documents.')
    return [file.split('/')[-1] for file in available_docs]

def list_available_documents():
    """List available .txt and .csv documents in the repository."""
    api = HfApi()
    files = api.list_repo_files(repo_id=repo_id)
    docs = [f for f in files if f.endswith('.txt') or f.endswith('.csv')]
    return docs

def get_document_content(document_name):
    csv.field_size_limit(sys.maxsize)
    file_path = hf_hub_download(repo_id=repo_id, filename=document_name, use_auth_token=False)
    content = []

    with open(file_path, mode='r', encoding='utf-8') as f:
        if document_name.endswith('.csv'):
            reader = csv.DictReader(f)
            for row in reader:
                # Directly take the text from 'Full_Document', no JSON parsing needed
                content.append(row.get('Full-Document', ''))
        elif document_name.endswith('.txt'):
            content = f.read()
    os.remove(file_path)
    return content
      

def load_and_process_document(content, document_name):
    """
    Process document content (either a single string or a list of strings) into a structured dictionary.
    Each paragraph is indexed by its order.
    """
    # If content is a single string (from a .txt file), split into paragraphs
    if isinstance(content, str):
        paragraphs = content.split('\n\n')
    elif isinstance(content, list):
        # Assume each item in the list is a separate paragraph/document
        paragraphs = content
    else:
        raise ValueError("Unsupported content type. Content must be a string or a list of strings.")

    # Filter out any empty paragraphs
    paragraphs = [p for p in paragraphs if p.strip()]

    # Logging for verification
    print(f'Total paragraphs or documents: {len(paragraphs)}')
    for i, paragraph in enumerate(paragraphs[:5]):  # Example: log first 5 paragraphs/documents
        preview = paragraph[:30] + "..." if len(paragraph) > 30 else paragraph
        print(f'Preview of paragraph/document {i+1}: "{preview}"')
    
    # Create a dictionary where each paragraph/document is indexed
    paragraph_dict = {i: paragraph for i, paragraph in enumerate(paragraphs)}
    
    # Save processed content to a binary file in the local 'data' directory
    data_dir = os.path.join(os.getcwd(), './data')
    os.makedirs(data_dir, exist_ok=True)
    file_path = os.path.join(data_dir, f'{document_name}.pkl')
    
    with open(file_path, 'wb') as file:
        pickle.dump(paragraph_dict, file)
    
    return paragraph_dict

# Function to load processed document content from a binary file
def load_paragraph_dict_from_file(document_name, data_dir='./data'):
    # Construct the full path to the binary file
    file_path = os.path.join(data_dir, f'{document_name}.pkl')

    # Check if the file exists
    if os.path.isfile(file_path):
        # Load and return the paragraph dictionary from the file
        with open(file_path, 'rb') as file:
            paragraph_dict = pickle.load(file)
        return paragraph_dict

    # If the file does not exist, return None
    return None

    




            
            
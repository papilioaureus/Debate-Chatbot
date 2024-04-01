import os
import requests
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from huggingface_hub import HfApi, hf_hub_download, HfFolder
import csv
from io import StringIO
import re 
from langchain.text_splitter import CharacterTextSplitter


load_dotenv('.env')

app = Flask(__name__)

repo_id = 'asaurasieu/debatebot'
repo_url = 'https://huggingface.co/asaurasieu/debatebot'

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
      

def load_and_process_document(content, chunk_size=5000, chunk_overlap=10):
    """
    Splits the 'Full_Document' content into manageable chunks for vector embedding.

    Args:
    full_document (str): The string content of the 'Full_Document'.
    chunk_size (int): The size of each chunk in characters.
    chunk_overlap (int): The number of characters that overlap between consecutive chunks.

    Returns:
    list of str: The list of text chunks after splitting.
    """
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    text_chunks = text_splitter.split_text(content)
    return text_chunks



            
            
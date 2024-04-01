import os
import requests
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from huggingface_hub import HfApi, hf_hub_download, HfFolder
import csv
from io import StringIO
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
    with open(file_path, mode='r', encoding='utf-8') as f:
        if document_name.endswith('.csv'):
            # Read the CSV file into a list of dictionaries
            reader = csv.DictReader(f)
            content = list(reader)  # Each row is a dict
        else:
            content = f.read()
    os.remove(file_path)
    return content


def load_and_process_document(text_content):
    """
    Directly process the text content without loading from a file.
    Split the provided text content into manageable chunks.
    """
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
    # Directly split the text content instead of loading from a file.
    processed_documents = text_splitter.split_documents([text_content])  # Ensure text_content is a list
    return processed_documents
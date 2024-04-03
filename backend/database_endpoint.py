import os
import requests
import nltk
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import logging
from bs4 import BeautifulSoup
from huggingface_hub import HfApi, hf_hub_download, HfFolder
import csv
from io import StringIO
import sys 
import re 
import pickle
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk.util import ngrams
from nltk import pos_tag, ne_chunk
from datetime import datetime
import pandas as pd
import pickle
import nltk
import ssl
import ast  # For safely evaluating strings containing Python expressions


try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Now you can safely call the nltk.download() functions
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('maxent_ne_chunker')
nltk.download('words')


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
    docs = [f for f in files if f.endswith('.txt') or f.endswith('_.csv')]
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

def extract_keywords_from_text(text):
    start_time = datetime.now()
    stop_words = set(stopwords.words('english'))

    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    
    # Initialize a set to store unique keywords
    keywords = set()
    
    for sentence in sentences:
        words = word_tokenize(sentence)
        pos_tags = pos_tag(words)
        
        for chunk in ne_chunk(pos_tags, binary=False):
            if hasattr(chunk, 'label'):
                keywords.add(" ".join(c[0] for c in chunk))
            else:
                word, tag = chunk
                if tag in ['NNP', 'NNPS'] and word.lower() not in stop_words:
                    keywords.add(word)
        
        filtered_words = [word for word in words if word[0].isupper()]
        
        # Extracting N-Grams (bigrams and trigrams as example)
        for n in range(2, 4):
            n_grams = ngrams(filtered_words, n)
            for grams in n_grams:
                joined_grams = " ".join(grams)
                # Check if the joined grams start with an uppercase letter (simple heuristic)
                if joined_grams[0].isupper():
                    keywords.add(joined_grams)
        
        # Adding individual proper nouns and specific nouns
        proper_nouns_and_nouns = [word for word, tag in pos_tags if tag in ['NNP', 'NNPS', 'NN', 'CD']]
        keywords.update(proper_nouns_and_nouns)
        
    # Optionally, filter out stopwords from the keywords
    filtered_keywords = [kw for kw in keywords if kw.lower() not in stop_words]
    
    end_time = datetime.now()
    logging.info("Total processing time: {}".format(end_time - start_time))
    return list(filtered_keywords)
    


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



def find_most_relevant_document(user_input_keywords):
    # Load the CSV file
    csv_file_path = '/Users/cristina/Documents/GitHub/Debate-Chatbot/backend/data/keywords_count_merged.csv'
    df = pd.read_csv(csv_file_path)

    # Initialize a dictionary to keep track of scores for each document
    document_scores = {}

    # Iterate over each row in the DataFrame
    for _, row in df.iterrows():
        original_filename = row['OriginalDebateFileName']
        # Safely evaluate the string representation of the list of tuples in 'Keywords_Counts' column
        keywords_counts = ast.literal_eval(row['Keywords_Counts'])
        
        # Initialize score for this document
        score = 0
        
        # Iterate over each keyword and its count in the document
        for keyword, count in keywords_counts:
            # If the keyword from the document is in the user input, add its count to the score
            if keyword in user_input_keywords:
                score += count
        
        # Update the document score
        document_scores[original_filename] = score

    # Find the document with the highest score
    most_relevant_document = max(document_scores, key=document_scores.get)

    return most_relevant_document


def load_and_process_document(content, document_name):
    """
    Process document content into a structured dictionary with indexed paragraphs.
    Each entry in the dictionary includes the paragraph text and extracted keywords,
    along with the original document name.
    """
    if isinstance(content, str):
        paragraphs = content.split('\n\n')
    elif isinstance(content, list):
        paragraphs = content
    else:
        raise ValueError("Unsupported content type. Content must be a string or a list of strings.")

    paragraphs = [p for p in paragraphs if p.strip()]

    # Create a dictionary to store processed paragraphs and their keywords
    paragraph_dict = {}
    for i, paragraph in enumerate(paragraphs):
        keywords = extract_keywords_from_text(paragraph)
        paragraph_dict[i] = {'chunk': paragraph, 'keywords': keywords}

    # Save processed content with document name reference
    data_dir = os.path.join(os.getcwd(), 'data')
    os.makedirs(data_dir, exist_ok=True)
    file_path = os.path.join(data_dir, f'{document_name}.pkl')
    
    # Include document_name in the structure saved to the .pkl file
    data_to_save = {'OriginalDebateFileName': document_name, 'paragraphs': paragraph_dict}
    
    with open(file_path, 'wb') as file:
        pickle.dump(data_to_save, file)
    
    return data_to_save

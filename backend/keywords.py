from collections import defaultdict
import os 
import logging
from flask import jsonify
from database_endpoint import (list_available_documents, get_document_content,
                               load_and_process_document, load_paragraph_dict_from_file, 
                               extract_keywords_from_text)

logging.basicConfig(level=logging.INFO)


keywords_to_chunks_index = defaultdict(list)

# Path to the data directory
data_dir = './data'

def index_text_chunks(text_chunks):
    return list(text_chunks.keys())

def process_document_chunks(paragraph_dict):
    chunk_keywords_index = []

    # {index: {'chunk': text, 'keywords': [keywords]}}
    for index, data in paragraph_dict.items():
        chunk = data['chunk']  # Now extracting 'chunk' from the dictionary
        chunk_keywords_index.append({
            'index': index,
            'chunk': chunk,
            'keywords': data['keywords']  # Directly use the provided keywords
        })

    return chunk_keywords_index


def populate_keywords_to_chunks_index():
    logging.info("Populating the keywords to chunks index.")
    document_names = list_available_documents()
    
    for document_name in document_names:
        # Process each document to load its content and extract paragraph data
        paragraph_dict = load_paragraph_dict_from_file(document_name)
        if not paragraph_dict:
            raw_content = get_document_content(document_name)
            paragraph_dict = load_and_process_document(raw_content, document_name)
                    
        for index, data in paragraph_dict.items():
            for keyword in data['keywords']:
                keywords_to_chunks_index[keyword].append((document_name, index))
    logging.info("Finished populating the keywords to chunks index.")


def process_and_store_document_content(document_name):
    raw_content = get_document_content(document_name)  
    load_and_process_document(raw_content, document_name) 
    
    
def load_and_index_documents():
    """Load index from file if it exists, otherwise create it."""
    document_names = list_available_documents()
    for document_name in document_names:
        # Check if the document has already been processed and indexed
        if not load_paragraph_dict_from_file(document_name):
            raw_content = get_document_content(document_name)
            paragraph_dict = load_and_process_document(raw_content, document_name)
            chunk_keywords_index = process_document_chunks(paragraph_dict)
            populate_keywords_to_chunks_index(document_name, chunk_keywords_index)
        else:
            print(f"Document {document_name} has already been indexed.")
 
        
def search_for_query(query):
    query_keywords = extract_keywords_from_text(query)
    logging.info(f"Extracted query keywords: {query_keywords}")
    query_keywords_set = set(query_keywords)  # Convert list to set for efficient comparison

    potential_matches = {}  # To keep track of potential matches before scoring

    # Aggregate potential matches based on any matching keyword in the index
    for keyword in query_keywords:
        if keyword in keywords_to_chunks_index:
            for document_name, chunk_index in keywords_to_chunks_index[keyword]:
                if (document_name, chunk_index) not in potential_matches:
                    potential_matches[(document_name, chunk_index)] = 0

    best_match = None  # To keep track of the best match across all documents
    highest_score = -1  # Initial score to ensure any real match will replace this

    # Evaluate each potential match based on the query context
    for (document_name, chunk_index), _ in potential_matches.items():
        paragraph_dict = load_paragraph_dict_from_file(document_name)
        if not paragraph_dict:
            logging.error(f"Could not load paragraph dict for document: {document_name}")
            continue
        
        chunk_data = paragraph_dict.get(str(chunk_index), None)  # Ensure string index is used
        if chunk_data:
            paragraph_keywords_set = set(chunk_data['keywords'])
            intersection = query_keywords_set.intersection(paragraph_keywords_set)
            score = len(intersection)

            if score > highest_score:
                best_match = {
                    'document_name': document_name,
                    'chunk_index': chunk_index,
                    'keywords': chunk_data['keywords'],
                    'score': score
                }
                highest_score = score

    return best_match if best_match else {}
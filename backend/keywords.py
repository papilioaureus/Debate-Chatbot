from collections import defaultdict
import os 
import logging
from flask import jsonify
from database_endpoint import (list_available_documents, get_document_content,
                               load_and_process_document, load_paragraph_dict_from_file, 
                               extract_keywords_from_text, find_most_relevant_document)

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
        paragraph_dict = load_paragraph_dict_from_file(document_name)
        if paragraph_dict and 'paragraphs' in paragraph_dict:  # Ensure the paragraph_dict is not None and contains 'paragraphs'
            for index, data in paragraph_dict['paragraphs'].items():
                for keyword in data['keywords']:
                    keywords_to_chunks_index[keyword].append((document_name, index))
        else:
            logging.error(f"Document {document_name} data is invalid or missing 'paragraphs' key.")
    
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
 
        
def search_for_query(query, most_relevant_document):
    print("HERE0")
    query_keywords = extract_keywords_from_text(query)
    logging.info(f"Extracted query keywords: {query_keywords}")
    print("HERE1")
    
    # Use the new function to find the most relevant document
    most_relevant_document = find_most_relevant_document(query_keywords)
    logging.info(f"Most relevant document: {most_relevant_document}")

    print("HERE2")
    
    best_match = None
    highest_score = -1

    for keyword in query_keywords:
        if keyword in keywords_to_chunks_index:
            
            logging.info(f"Keyword found in index: {keyword}")
            for doc_name, chunk_index in keywords_to_chunks_index[keyword]:
                if doc_name == most_relevant_document:  # Filter by the most relevant document
                    paragraph_dict = load_paragraph_dict_from_file(doc_name)
                    if not paragraph_dict:
                        logging.error(f"Could not load paragraph_dict for document: {doc_name}")
                        continue

                    chunk_data = paragraph_dict['paragraphs'].get(chunk_index, None)
                    if chunk_data:
                        # Count how many query keywords are in this paragraph's keywords
                        score = sum(kw in chunk_data['keywords'] for kw in query_keywords)
                        # Update best match if this paragraph has a higher score
                        if score > highest_score:
                            best_match = {
                                'document_name': doc_name,
                                'chunk_index': chunk_index,
                                'chunk': chunk_data['chunk'],
                                'keywords': chunk_data['keywords'],
                                'score': score
                            }
                            highest_score = score
        else:
            logging.info(f"Keyword '{keyword}' not found in index")

        if best_match:
            logging.info(f"Best match found: {best_match}")
        else:
            logging.info("No match found")
    print("HERE3")
    return best_match if best_match else {}




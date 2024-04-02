from collections import defaultdict
import nltk
import os
from flask import jsonify
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from database_endpoint import list_available_documents, get_document_content,load_and_process_document, load_paragraph_dict_from_file


nltk.download('punkt')
nltk.download('stopwords')


# Global index mapping keywords to document chunks
keywords_to_chunks_index = defaultdict(list)

# Path to the data directory
data_dir = './data'


def index_text_chunks(text_chunks):
    return list(text_chunks.keys())

def extract_keywords_from_text(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    keywords = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]
    return list(set(keywords)) 


def process_document_chunks(paragraph_dict):
    chunk_keywords_index = []

    for index, chunk in paragraph_dict.items():
        chunk_keywords = extract_keywords_from_text(chunk)
        chunk_keywords_index.append({
            'index': index,
            'chunk': chunk,  
            'keywords': chunk_keywords
        })

    return chunk_keywords_index


def index_document_chunks(document_name, chunk_keywords_index):
    for entry in chunk_keywords_index:
        index, chunk, keywords = entry['index'], entry['chunk'], entry['keywords']
        for keyword in keywords:
            # Append document name and paragraph index to the keyword entry
            keywords_to_chunks_index[keyword].append((document_name, index))


def process_and_store_document_content(document_name):
    # This function will not store the data as it's assumed to be handled by load_and_process_document
    raw_content = get_document_content(document_name)  
    load_and_process_document(raw_content, document_name) 
    
    
def load_and_index_documents():
    """Function to load and index documents from the repository, only if they're not already indexed."""
    document_names = list_available_documents()
    for document_name in document_names:
        # Construct the file path for the indexed document
        file_path = os.path.join(data_dir, f'{document_name}.pkl')

        # Check if the file already exists
        if os.path.isfile(file_path):
            print(f"Index file for {document_name} already exists. Skipping indexing.")
            continue

        print(f"Indexing document: {document_name}")
        raw_content = get_document_content(document_name)
        paragraph_dict = load_and_process_document(raw_content, document_name)
        chunk_keywords_index = process_document_chunks(paragraph_dict)
        index_document_chunks(document_name, chunk_keywords_index)
        
def search_for_query(query):
    query_keywords = extract_keywords_from_text(query)
    print(f"Query Keywords: {query_keywords}")
    matched_chunks = defaultdict(list)

    for keyword in query_keywords:
        if keyword in keywords_to_chunks_index:
            for document_name, chunk_index in keywords_to_chunks_index[keyword]:
                paragraph_dict = load_paragraph_dict_from_file(document_name)
                if paragraph_dict:
                    paragraph_text = paragraph_dict.get(chunk_index)
                    if paragraph_text:
                        matched_chunks[document_name].append(chunk_index)

    # Retrieve actual chunk content based on matched indices
    matched_content = defaultdict(dict)
    for document_name, indices in matched_chunks.items():
        paragraph_dict = load_paragraph_dict_from_file(document_name)  # Move this inside the loop
        for index in indices:
            matched_content[document_name][index] = paragraph_dict.get(index)

    # Return the matched content as a dictionary
    return dict(matched_content)  # Convert defaultdict to a regular dictionary for output



from collections import defaultdict
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from database_endpoint import load_and_process_document

# Download necessary NLTK data (if not already done)
nltk.download('punkt')
nltk.download('stopwords')

def index_text_chunks(text_chunks):
    indexes = list(range(len(text_chunks)))
    return indexes

def extract_keywords_from_text(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    keywords = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]
    return list(set(keywords))  # Return unique keywords

def process_document_chunks(content):
    chunks = load_and_process_document(content)  # Load and process document to get chunks
    chunk_indexes = index_text_chunks(chunks)  # Use the provided index function
    chunk_keywords_index = []

    for index, chunk in zip(chunk_indexes, chunks):
        chunk_keywords = extract_keywords_from_text(chunk)
        chunk_keywords_index.append({
            'index': index,  
            'chunk': chunk,
            'keywords': chunk_keywords
        })

    return chunk_keywords_index

# Global index mapping keywords to document chunks
keywords_to_chunks_index = defaultdict(list)

def index_document_chunks(document_name, chunk_keywords_index):
    for entry in chunk_keywords_index:
        index, chunk, keywords = entry['index'], entry['chunk'], entry['keywords']
        for keyword in keywords:
            # Append document name and chunk index to the keyword entry
            keywords_to_chunks_index[keyword].append((document_name, index))

def search_for_query(query):
    query_keywords = extract_keywords_from_text(query)
    matched_chunks = defaultdict(list)

    for keyword in query_keywords:
        if keyword in keywords_to_chunks_index:
            for document_name, chunk_index in keywords_to_chunks_index[keyword]:
                matched_chunks[document_name].append(chunk_index)

    # Process matched_chunks to retrieve or summarize the actual chunk content as needed
    return matched_chunks

from flask import Flask, request, jsonify
from database_endpoint import  get_document_content, load_and_process_document
import openai
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


load_dotenv('.env')

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

vectordb = None
pdf_qa = None

class DocumentChunk:
    def __init__(self, content, metadata=None):
        self.page_content = content
        self.metadata = metadata if metadata is not None else {}

def initialize_vectordb_with_document(document_name):
    content = get_document_content(document_name)
    
    # Create DocumentChunk objects from the content
    document_chunks = load_and_process_document(document_path)
    
    # Pass the list of DocumentChunk objects to load_and_process_document
    processed_documents = load_and_process_document(document_chunks)
    
    # Initialize Chroma with the processed document chunks.
    vectordb = Chroma.from_documents(processed_documents, embedding=OpenAIEmbeddings(), persist_directory="./data")
    vectordb.persist()
    
    return vectordb

def get_relevant_content_from_vectordb(document_name, user_message):
    vectordb = initialize_vectordb_with_document(document_name)
    # Adjust `top_k` based on how many top results you want to consider.
    top_k = 3
    results = vectordb.search(user_message, top_k=top_k)

    if results:
        # Format and contextualize the results.
        formatted_results = []
        for i, result in enumerate(results, start=1):
            # Assuming 'content' is the text of the document chunk.
            content = result['content']
            formatted_results.append(f"Result {i}: {content}\n")
        
        relevant_content = "\n".join(formatted_results)
        return relevant_content
    else:
        return "Sorry, I couldn't find any relevant information in the document."

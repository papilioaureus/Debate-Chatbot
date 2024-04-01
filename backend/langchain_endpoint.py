from flask import Flask, request, jsonify
import openai
import os
from database_endpoint import get_document_content, load_and_process_document
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv('.env')

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


vectordb_cache = {}

def get_document_content_as_string(document_name):
    content_list = get_document_content(document_name)
    # Join the list into a single string if necessary
    if isinstance(content_list, list):
        return ' '.join(filter(None, content_list))
    else:
        return content_list

def initialize_vectordb_with_document(document_name):
    # Get the document content as a single string
    content = get_document_content_as_string(document_name)
    processed_documents = load_and_process_document(content)
    # Initialize the vector database with these chunks
    vectordb = Chroma.from_documents(processed_documents, embedding=OpenAIEmbeddings(), persist_directory=f"./data/{document_name}")
    vectordb.persist()
    return vectordb
from flask import Flask, jsonify, request
from database_endpoint import list_available_documents, get_document_content,load_and_process_document, load_paragraph_dict_from_file
from keywords import search_for_query, load_and_index_documents
from request import url 
import openai
import logging
import json
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

def load_and_index_documents():
    # Your document loading and indexing code here...
    print("Documents have been loaded and indexed.")

# Run the function once at the start of your application
load_and_index_documents()

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Langchain API!'})

@app.route('/documents', methods=['GET'])
def list_documents():
    """Endpoint to list available documents."""
    docs = list_available_documents()
    return jsonify(docs)

@app.route('/documents/<string:document_name>', methods=['GET'])
def get_document(document_name):
    # List available documents to check if the requested document exists
    available_docs = list_available_documents()

    # Check if the document_name exists in the available documents
    if document_name in available_docs:
        # Try to load processed content from the file
        processed_content = load_paragraph_dict_from_file(document_name)
        if processed_content is None:  # If the content is not processed, process it now
            content = get_document_content(document_name)
            processed_content = load_and_process_document(content, document_name)
        return jsonify(processed_content)
    else:
        return jsonify({'error': 'Document not found.'}),


@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def catch_all(path):
    if path == 'documents':
        return list_available_documents()
    else:
        return jsonify({'message': 'Please access the /documents endpoint for the available documents.'})

logging.basicConfig(level=logging.INFO)

    
@app.route('/ask', methods=['POST'])
def ask_question():
    user_input = request.json.get('user_input')
    matched_content = search_for_query(user_input)
    print("matched_content: ", matched_content)
    relevant_content = []

    for document_name, chunk_indices in matched_content.items():
        for index in chunk_indices:
            paragraph_dict = load_paragraph_dict_from_file(document_name)
            print("paragraph_dict: ", paragraph_dict)
            if paragraph_dict:
                relevant_content.append(paragraph_dict.get(index, ''))

    combined_content = " ".join(relevant_content)
    messages = [
        {"role": "system", "content": "You are a knowledgeable assistant."},
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": f"Based on the document content: {combined_content}"}
    ]

    # Assuming you have already configured the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Adjust model version if necessary
        messages=messages,
        temperature=0.7
    )

    last_message = response.choices[-1]['message']['content']
    return jsonify({'answer': last_message.strip()})

    
    
# @app.route('/search')
# def search():
#     query = request.args.get('query', '')
#     matched_content = search_for_query(query)
    
#     # Enhance the response structure to include document names and paragraph indices
#     enriched_response = []
#     for document_name, paragraphs in matched_content.items():
#         for index, text in paragraphs.items():
#             enriched_response.append({
#                 'document': document_name,
#                 'paragraph_index': index,
#                 'text': text
#             })

#     return jsonify({'matches': enriched_response})

   
if __name__ == '__main__':
    app.run(debug=True, port=5000)
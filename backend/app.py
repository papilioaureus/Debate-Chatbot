from flask import Flask, jsonify, request
from database_endpoint import list_available_documents, get_document_content,load_and_process_document
from keywords import search_for_query
from request import url 
import openai
import logging
import json
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

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
    try:
        # Retrieve content from the document
        raw_content = get_document_content(document_name)
        processed_content = []

        # Process the content based on its type
        if isinstance(raw_content, list):
            # Process each document's content for embedding if it's from a CSV
            processed_content = [load_and_process_document(doc) for doc in raw_content if doc.strip()]
        elif isinstance(raw_content, str) and raw_content.strip():
            # If it's a string and contains something other than whitespace
            try:
                # Attempt to parse it as JSON and extract the 'content' key
                json_content = json.loads(raw_content)
                text_content = json_content.get('content', '')
                # Process the extracted text for embedding
                processed_content = load_and_process_document(text_content)
            except json.JSONDecodeError:
                # If it's not JSON, it might be plain text, so process it directly
                processed_content = load_and_process_document(raw_content)

        # Return the processed content
        return jsonify(processed_content)

    except Exception as e:
        # Handle any unexpected errors
        return jsonify({'error': str(e)}), 500


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
    # Search for query in the document chunks and get matched chunk indices
    
    matched_chunks_info = search_for_query(user_input)
    relevant_content = []
    for document_name, chunk_indices in matched_chunks_info.items():
        # Ensure to modify load_and_process_document to accept a chunk_index parameter
        for chunk_index in chunk_indices:
            # Now the function is expected to retrieve a specific chunk by index
            chunk_content = load_and_process_document(document_name, chunk_index=chunk_index)
            relevant_content.append(chunk_content)

    # Combine all relevant content into a single string for the response
    combined_content = " ".join(relevant_content)

    messages = [
        {"role": "system", "content": "You are a knowledgeable assistant."},
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": f"Based on the document content: {combined_content}"}
    ]

    # Make a request to the OpenAI API to get the response using the chat model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Adjust model version if necessary
        messages=messages,
        temperature=0.7
    )

    # Extract the assistant's last message as the response
    last_message = response.choices[-1]['message']['content']
    
    # Return the assistant's response along with the source information
    return jsonify({'answer': last_message.strip()})
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)
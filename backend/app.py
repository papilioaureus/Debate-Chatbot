from flask import Flask, jsonify, request
from database_endpoint import list_available_documents, get_document_content
from langchain_endpoint import get_relevant_content_from_vectordb
import openai

app = Flask(__name__)

@app.route('/documents', methods=['GET'])
def list_documents():
    """Endpoint to list available documents."""
    docs = list_available_documents()
    return jsonify(docs)

@app.route('/documents/<string:document_name>', methods=['GET'])
def get_document(document_name):
    content = get_document_content(document_name)
    if isinstance(content, list):
        # Return a list of dicts if it's a CSV file
        return jsonify(content)
    else:
        # Return a string wrapped in a dict if it's a text file
        return jsonify({"content": content})


@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def catch_all(path):
    if path == 'documents':
        return list_available_documents()
    else:
        return jsonify({'message': 'Please access the /documents endpoint for the available documents.'})
    
@app.route('/chat', methods=['POST'])
def chat_endpoint():
    user_input = request.json.get('message', '')
    document_name = request.json.get('document_name', '')

    relevant_content = get_relevant_content_from_vectordb(document_name, user_input)

    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=f"Based on the document, here is the information relevant to your question:\n{relevant_content}\n\nCan you provide more detailed information on this?",
        max_tokens=4000,
        temperature=0.7
    )
    
    answer = response.choices[0].text.strip()
    return jsonify({'response': answer})
    
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)
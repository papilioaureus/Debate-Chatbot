from flask import Flask, send_from_directory
from flask import Flask, request, jsonify
from debatebot_api import app
from chatbot import get_response

@app.route('/')
def index():
    return send_from_directory('frontend', '/public/index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    response = get_response(user_input)  
    return jsonify({'response': response})

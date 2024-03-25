from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
from applicationinsights.flask.ext import AppInsights
from huggingface_hub import HfApi, hf_hub_download

app = Flask(__name__)

load_dotenv()

# Environment configuration setup
if os.getenv('ENV') == 'local':
    print("Running in local mode")
    app.config.from_object('config.LocalConfig')
elif os.getenv('ENV') == 'dev':
    print("Running in development mode")
    app.config.from_object('config.DevelopmentConfig')
elif os.getenv('ENV') == 'ghci':
    print("Running in github mode")
    app.config.from_object('config.GithubCIConfig')

CORS(app)

# Initializing app insights and flushing after each request in dev mode
if os.getenv('ENV') == 'dev':
    app_insights = AppInsights(app)

    @app.after_request
    def after_request(response):
        app_insights.flush()
        return response

# Example endpoint to retrieve a document from Hugging Face Hub
@app.route('/get-document', methods=['GET'])
def get_document():
    try:
        # Specify the path to your file within the repository
        file_path = 'path/to/your/document.txt'  # Update this path accordingly
        
        # Specify your Hugging Face repository ID
        repo_id = 'asaurasieu/debatebot'
        
        # Download the file
        file_content = hf_hub_download(repo_id=repo_id, filename=file_path, cache_dir="./tmp")
        
        with open(file_content, 'r', encoding='utf-8') as file:
            content = file.read()
        
        return jsonify({"status": "success", "content": content}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

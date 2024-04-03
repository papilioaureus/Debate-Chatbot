import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai


load_dotenv('.env')

app = Flask(__name__)

# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set the URL of your Flask endpoint
url = "http://127.0.0.1:5000"

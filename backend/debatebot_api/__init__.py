from flask import Flask
import os
from flask_cors import CORS

app = Flask(__name__, static_folder='public')
CORS(app, resources={r"/chat": {"origins": "http://localhost:3000"}})
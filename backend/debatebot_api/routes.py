from flask import Flask, send_from_directory
from debatebot_api import app

@app.route('/')
def index():
    return send_from_directory('frontend', '/public/index.html')


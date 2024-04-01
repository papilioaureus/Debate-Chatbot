import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import json
from flask_testing import TestCase
import pytest
from app import app  

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_endpoint(client):
    """Test the home endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {'message': 'Welcome to the Langchain API!'}

def test_list_documents(client):
    """Test the documents listing endpoint."""
    response = client.get('/documents')
    assert response.status_code == 200
    assert isinstance(response.json, list)  
    
class TestGetDocument(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_get_document(self):
        document_name = 'Ukraine_text.txt'
        response = self.client.get(f'/documents/{document_name}')
        self.assertEqual(response.status_code, 200)
 

def test_get_document_failure(client):
    """Test retrieving a non-existing document."""
    response = client.get('/documents/non_existing_document')
    assert response.status_code == 500
    assert 'error' in response.json 

def test_ask_question(client):
    """Test the ask question endpoint."""
    data = {"user_input": "Example question"}
    response = client.post('/ask', json=data)
    assert response.status_code == 200
  

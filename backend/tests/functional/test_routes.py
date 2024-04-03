import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import json
from flask_testing import TestCase
import pytest
from app import app
from unittest.mock import patch, MagicMock


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_endpoint(client):
    """Test the home endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {'message': 'Welcome to the API!'}

def test_list_documents(client):
    """Test the documents listing endpoint."""
    response = client.get('/documents')
    assert response.status_code == 200
    assert isinstance(response.json.get('documents'), list)
    

def test_get_existing_document(client, mocker):
    # Mock `list_available_documents` to simulate the document exists
    mocker.patch('app.list_available_documents', return_value=['existing_document'])
    # Mock `load_paragraph_dict_from_file` to return a predefined dictionary if the file exists
    mocker.patch('app.load_paragraph_dict_from_file', return_value={'paragraph1': 'Content of paragraph1'})

    response = client.get('/documents/existing_document')
    assert response.status_code == 200
    assert response.json == {'paragraph1': 'Content of paragraph1'}

def test_get_nonexistent_document(client, mocker):
    # Mock `list_available_documents` to simulate the document does not exist
    mocker.patch('app.list_available_documents', return_value=['some_document'])

    response = client.get('/documents/nonexistent_document')

    # Check if the status code is 404 Not Found
    assert response.status_code == 404, "Expected 404 Not Found for a nonexistent document."

    # Assuming your application is set up to return a JSON response with an error message
    assert response.json == {'error': 'Document not found.'}, "Unexpected error message returned."

def test_get_unprocessed_document(client, mocker):
    # Mock `list_available_documents` and `load_paragraph_dict_from_file` for an unprocessed document
    mocker.patch('app.list_available_documents', return_value=['unprocessed_document'])
    mocker.patch('app.load_paragraph_dict_from_file', side_effect=[None, {'paragraph1': 'Processed content'}])
    # Mock `get_document_content` to simulate fetching raw content
    mocker.patch('app.get_document_content', return_value="Raw document content")
    # Mock `load_and_process_document` to simulate processing of the document
    mocker.patch('app.load_and_process_document', return_value={'paragraph1': 'Processed content'})

    response = client.get('/documents/unprocessed_document')
    assert response.status_code == 200
    assert response.json == {'paragraph1': 'Processed content'}


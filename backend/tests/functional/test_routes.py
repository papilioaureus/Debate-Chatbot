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
    


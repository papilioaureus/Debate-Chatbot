import os
import sys

# Adding the path of the models directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest 
from unittest.mock import patch, MagicMock
from backend.database_endpoint import list_hf_repository_files, list_available_documents, load_and_process_document


@pytest.fixture
def mock_response():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.text = '<html><body><a class="Link--active" href="/repo/file1.txt">file1.txt</a><a class="Link--active" href="/repo/file2.csv">file2.csv</a></body></html>'
        mock_get.return_value = mock_response
        yield mock_get

def test_list_hf_repository_files(mock_response):
    expected_files = ['file1.txt', 'file2.csv']
    files = list_hf_repository_files('https://huggingface.co/asaurasieu/debatebot')
    assert files == expected_files
    mock_response.assert_called_once()
    

@pytest.fixture
def mock_api():
    with patch('database_endpoint.HfApi.list_repo_files') as mock_list_repo_files:
        mock_list_repo_files.return_value = ['document1.txt', 'data.csv', 'image.png']
        yield mock_list_repo_files

def test_list_available_documents(mock_api):
    expected_docs = ['document1.txt', 'data.csv']
    docs = list_available_documents()
    assert docs == expected_docs
    mock_api.assert_called_once()
    
def test_load_and_process_document():
    content = "This is a test document content for testing."
    expected_chunks = ["This is a test document content for testing."]  
    chunks = load_and_process_document(content, chunk_size=5000, chunk_overlap=10)
    assert chunks == expected_chunks
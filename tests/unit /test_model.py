import os
import pytest
import sys
from unittest.mock import patch

# Adding the path of the models directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../debchatlib/models')))

# Importing necessary functions from the chatbot module
from chatbot import list_hf_repository_files, select_document, fetch_hf_documents

# This test checks if the function list_hf_repository_files correctly returns a list of files
# The function get_access_token is patched to return a dummy token
@patch('chatbot.get_access_token', return_value='dummy_token')
def test_list_hf_repository_files(mock_get_access_token):
    repo_id = 'asaurasieu/debatebot'
    files = list_hf_repository_files(repo_id)
    assert isinstance(files, list)  

# This test checks if the function select_document correctly selects a document based on user input
# The built-in input function is patched to return "1"
@pytest.mark.parametrize(
    "docs", [['debate2015.csv', 'debate2019.csv']]
)
def test_select_document(docs, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "1")
    selected_doc = select_document(docs)
    assert selected_doc == 'debate2015.csv' 

# This test checks if the function fetch_hf_documents correctly fetches a document and saves it to a file
# The function get_access_token is patched to return a dummy token
@patch('chatbot.get_access_token', return_value='dummy_token')
def test_fetch_hf_documents(mock_get_access_token):
    repo_id = 'asaurasieu/debatebot'
    filename = 'debate2015.csv'  # Update this to the filename you want to test
    file_path = fetch_hf_documents(repo_id, filename)
    assert os.path.exists(file_path)  # Asserting that the file exists
    
    
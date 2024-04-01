import os
import pytest 
import sys
from unittest.mock import patch, Mock 
from database_endpoint import list_hf_repository_files, list_available_documents, load_and_process_document

# Adding the path of the models directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend/database_endpoint.py")))

# This test checks if the function list_hf_repository_files correctly returns a list of files
@patch('database_endpoint.get_access_token', return_value='dummy_token')
def test_list_hf_repository_files(mock_get_access_token):
    repo_url = 'https://huggingface.co/asaurasieu/debatebot'
    files = list_hf_repository_files(repo_url)
    assert isinstance(files, list)  

# This test checks if the function list_available_documents correctly returns a list of .txt and .csv documents
# The built-in input function is patched to return "1"
@pytest.mark.parametrize(
    "docs", [['debate2015.csv', 'debate2019.csv']]
)
def test_list_available_documents(docs, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "1")
    documents = list_available_documents()
    assert isinstance(documents, list)
    assert all(doc.endswith('.txt') or doc.endswith('.csv') for doc in documents)
    assert documents[0] == 'debate2015.csv'


def test_load_and_process_document():
    # Mocking the TextLoader and CharacterTextSplitter classes
    with patch('database_endpoint.CharacterTextSplitter') as MockCharacterTextSplitter:
        mock_loader = Mock()
        mock_splitter = Mock()
        MockCharacterTextSplitter.return_value = mock_splitter

        # Mocking the load and split_documents methods
        mock_loader.load.return_value = 'documents'
        mock_splitter.split_documents.return_value = 'split documents'

        # Testing the load_and_process_document function
        result = load_and_process_document('file_path')

        # Verifying that the load and split_documents methods were called
        mock_loader.load.assert_called_once()
        mock_splitter.split_documents.assert_called_once_with('documents')

        # Asserting that the function returned the expected result
        assert result == 'split documents'
import os
import sys

# Adding the path of the models directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest 
from unittest.mock import patch, MagicMock, mock_open
from database_endpoint import list_hf_repository_files, list_available_documents, load_and_process_document, get_document_content, load_paragraph_dict_from_file
import pickle 

@pytest.fixture
def mock_hf_hub_download(mocker):
    return mocker.patch('database_endpoint.hf_hub_download', return_value='path/to/temporary_file.csv')

@pytest.fixture
def mock_file_handling(mocker):
    # Ensure the CSV header matches what your function expects, including a row of data.
    csv_content = "Full-Document\nvalue1\n"
    mocker.patch('builtins.open', mock_open(read_data=csv_content))
    mocker.patch('os.remove')
    return mocker.patch('builtins.open', mock_open(read_data=csv_content), create=True)

def test_get_document_content_csv(mock_hf_hub_download, mock_file_handling):
    document_name = 'test_document.csv'
    expected_content = ['value1']  # The expected output matches the row in the mocked CSV

    content = get_document_content(document_name)

    # Assertions
    mock_file_handling.assert_called_once_with('path/to/temporary_file.csv', mode='r', encoding='utf-8')
    assert content == expected_content, f"Expected {expected_content}, got {content}"
    mock_hf_hub_download.assert_called_once()


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
    
    
    
# Test for processing single string content
def test_load_and_process_document_with_string():
    content = "Paragraph1\n\nParagraph2"  # Including an empty paragraph for filtering test
    document_name = 'test_document.txt'

    with patch("builtins.open", mock_open()) as mocked_file:
        with patch("os.makedirs") as mocked_makedirs:
            result = load_and_process_document(content, document_name)

            # Verifying directory creation
            mocked_makedirs.assert_called_once_with(os.path.join(os.getcwd(), './data'), exist_ok=True)

            # Verifying file operations
            mocked_file.assert_called_once_with(os.path.join(os.getcwd(), './data', f'{document_name}.pkl'), 'wb')

            # Check the result dictionary
            assert len(result) == 2, "Incorrect number of paragraphs processed"
            assert result[0] == "Paragraph1", "First paragraph mismatch"
            assert result[1] == "Paragraph2", "Second paragraph mismatch"

# Test when the file exists
def test_load_paragraph_dict_from_file_exists():
    document_name = 'existing_document'
    data_dir = './data'
    expected_dict = {'paragraph1': 'This is the first paragraph.', 'paragraph2': 'This is the second paragraph.'}

    with patch('os.path.isfile', return_value=True), \
         patch('builtins.open', mock_open(read_data=pickle.dumps(expected_dict))), \
         patch('pickle.load', return_value=expected_dict) as mock_pickle_load:
        
        result = load_paragraph_dict_from_file(document_name, data_dir)
        
        # Check if the result matches the expected output
        assert result == expected_dict, "The loaded dictionary does not match the expected output."
        # Ensure pickle.load was called once
        mock_pickle_load.assert_called_once()
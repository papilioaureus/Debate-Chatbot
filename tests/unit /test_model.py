from unittest.mock import patch, mock_open
import pytest
from chatbot import list_hf_repository_files, select_document, fetch_hf_documents, load_and_process_document

@pytest.fixture
def mock_api(mocker):
    return mocker.patch('chatbot.py.HfApi')

@pytest.fixture
def mock_env(mocker):
    return mocker.patch('chatbot.py.os.getenv', return_value='dummy_token')

@pytest.fixture
def mock_folder(mocker):
    return mocker.patch('chatbot.py.HfFolder')

def test_list_hf_repository_files(mock_api, mock_env, mock_folder):
    mock_api.list_repo_files.return_value = ['debate2019.csv', 'Ukraine_text.txt']
    result = list_hf_repository_files('asaurasieu/debatebot')
    assert result == ['debate2019.csv', 'Ukraine_text.tx']

def test_select_document(mocker):
    mocker.patch('builtins.input', return_value='1')
    docs = ['debate2015.csv', 'debate2019.csv']
    selected = select_document(docs)
    assert selected == 'debate2019.csv'

def test_fetch_hf_documents(mock_api):
    mock_api.hf_hub_download.return_value = '/asaurasieu/debatebot/debate2015.csv'
    result = fetch_hf_documents('asaurasieu/debatebot', 'debate2015.csv')
    assert result == '/asaurasieu/debatebot/debate2015.csv'

def test_load_and_process_document(mocker):
    mocker.patch('builtins.open', mock_open(read_data="This is a test."))
    mocker.patch('chatbot.py.TextLoader').return_value.load.return_value = ["This is a test."]
    mocker.patch('chatbot.py.CharacterTextSplitter').return_value.split_documents.return_value = ["This is a test."]
    result = load_and_process_document('/asaurasieu/debatebot/debate2019.csv')

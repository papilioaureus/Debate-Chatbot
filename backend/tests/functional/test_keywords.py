import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import pytest
from unittest.mock import patch, MagicMock, call
from keywords import (index_text_chunks, extract_keywords_from_text, 
                      process_document_chunks, populate_keywords_to_chunks_index, 
                      keywords_to_chunks_index, process_and_store_document_content, 
                      load_and_index_documents, search_for_query, keywords_to_chunks_index )

def test_index_text_chunks():

    input_dict = {
        'chunk1': 'Text of chunk 1',
        'chunk2': 'Text of chunk 2',
        'chunk3': 'Text of chunk 3',
    }
    
   
    expected_keys = ['chunk1', 'chunk2', 'chunk3']
    
    
    result_keys = index_text_chunks(input_dict)
    
  
    assert sorted(result_keys) == sorted(expected_keys), "The returned list of keys does not match the expected list."
        
    
def test_process_document_chunks():
    
    input_chunks = {
        '1': {'chunk': "Hello, world! This is a test.", 'keywords': ['hello', 'world', 'test']},
        '2': {'chunk': "Another test, with more words.", 'keywords': ['another', 'test', 'words']}
    }
  
    expected_output = [
        {
            'index': '1',
            'chunk': "Hello, world! This is a test.",
            'keywords': ['hello', 'world', 'test'] 
        },
        {
            'index': '2',
            'chunk': "Another test, with more words.",
            'keywords': ['another', 'test', 'words']  
        }
    ]

  
    result = process_document_chunks(input_chunks)

   
    assert result == expected_output, "The processed document chunks do not match the expected output."
    

    for chunk in result:
        chunk['keywords'] = set(chunk['keywords'])
   
    for chunk in expected_output:
        chunk['keywords'] = set(chunk['keywords'])
    
    assert result == expected_output, "The processed document chunks do not match the expected output."
    
    

def reset_global_index():
    global keywords_to_chunks_index
    keywords_to_chunks_index.clear()

def test_populate_keywords_to_chunks_index():
    reset_global_index()

    document_names = ["test_document_1", "test_document_2"]

    paragraph_dicts = [
        {'1': {'keywords': ['hello', 'world', 'test']}, '2': {'keywords': ['another', 'test', 'words']}},
        {'1': {'keywords': ['python', 'programming', 'language']}, '2': {'keywords': ['code', 'development', 'software']}}
    ]

    with patch('keywords.list_available_documents', return_value=document_names):
        with patch('keywords.load_paragraph_dict_from_file', side_effect=paragraph_dicts):
            populate_keywords_to_chunks_index()

    expected_index = {
        'hello': [('test_document_1', '1')],
        'world': [('test_document_1', '1')],
        'test': [('test_document_1', '1'), ('test_document_1', '2')],
        'another': [('test_document_1', '2')],
        'words': [('test_document_1', '2')],
        'python': [('test_document_2', '1')],
        'programming': [('test_document_2', '1')],
        'language': [('test_document_2', '1')],
        'code': [('test_document_2', '2')],
        'development': [('test_document_2', '2')],
        'software': [('test_document_2', '2')]
    }

    assert keywords_to_chunks_index == expected_index


def test_process_and_store_document_content():
    document_name = "sample_document"
    

    with patch('keywords.get_document_content') as mock_get_document_content, \
         patch('keywords.load_and_process_document') as mock_load_and_process_document:
        
       
        mock_get_document_content.return_value = "Fake document content"
        
    
        process_and_store_document_content(document_name)
        
      
        mock_get_document_content.assert_called_once_with(document_name)
        
        mock_load_and_process_document.assert_called_once_with("Fake document content", document_name)

def test_load_and_index_documents():
    
    available_documents = ["doc1", "doc2"]
    paragraph_dict = {
        '1': {'chunk': 'This is a text chunk.', 'keywords': ['chunk', 'text']}
    }

    def mock_load_paragraph_dict_from_file(document_name):
        if document_name == "doc1":
            return paragraph_dict  
        else:
            return None  

   
    with patch('keywords.list_available_documents', return_value=available_documents), \
         patch('keywords.load_paragraph_dict_from_file', side_effect=mock_load_paragraph_dict_from_file), \
         patch('keywords.get_document_content', return_value="Document content"), \
         patch('keywords.load_and_process_document', return_value=paragraph_dict), \
         patch('keywords.process_document_chunks', return_value=[{'index': '1', 'chunk': 'This is a text chunk.', 'keywords': ['chunk', 'text']}]), \
         patch('keywords.populate_keywords_to_chunks_index') as mock_populate_keywords_to_chunks_index:

       
        load_and_index_documents()

       
        assert mock_populate_keywords_to_chunks_index.call_count == 1
        mock_populate_keywords_to_chunks_index.assert_called_once_with("doc2", [{'index': '1', 'chunk': 'This is a text chunk.', 'keywords': ['chunk', 'text']}])

def reset_global_index():
    global keywords_to_chunks_index
    keywords_to_chunks_index.clear()

@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    reset_global_index()
    yield


def test_search_for_query():
    # Assume the real index uses integers for chunk indices
    keywords_to_chunks_index.update({
        'test': [('doc1', 1), ('doc2', 2)],
        'example': [('doc2', 2)],
    })

    mock_paragraphs = {
    'doc1': {
        1: {'chunk': "This is a test chunk in doc1.", 'keywords': []}
    },
    'doc2': {
        2: {'chunk': "This chunk contains test and example keywords.", 'keywords': ['test', 'example']}
    }
}

    # The expected result should also use integers for chunk indices
    expected_result = {
        'doc1': {
            1: {'chunk': "This is a test chunk in doc1.", 'keywords': []}
        },
        'doc2': {
            2: {'chunk': "This chunk contains test and example keywords.", 'keywords': ['test', 'example']}
        }
    }

    with patch('keywords.load_paragraph_dict_from_file', side_effect=lambda doc_name: mock_paragraphs.get(doc_name)) as mock_load_paragraph:
        result = search_for_query("test example")

        assert result == expected_result, "The search result does not match the expected output."

        unique_pairs = {('doc1', '1'), ('doc2', '2')} 
        assert mock_load_paragraph.call_count == len(unique_pairs), "load_paragraph_dict_from_file was not called as expected."
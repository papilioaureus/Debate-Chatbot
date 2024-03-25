import unittest
from unittest.mock import patch, MagicMock
from debchatlib.models.chatbot import list_hf_repository_files, select_document, fetch_hf_documents

class TestChatbot(unittest.TestCase):

    @patch('debchatlib.models.chatbot.HfApi')
    @patch('debchatlib.models.chatbot.HfFolder')
    def test_list_hf_repository_files(self, mock_folder, mock_api):
        mock_api().list_repo_files.return_value = ['file1', 'file2']
        result = list_hf_repository_files('test_repo')
        self.assertEqual(result, ['file1', 'file2'])

    @patch('debchatlib.models.chatbot.input', create=True)
    def test_select_document(self, mock_input):
        mock_input.return_value = '1'
        result = select_document(['doc1', 'doc2'])
        self.assertEqual(result, 'doc1')

    @patch('debchatlib.models.chatbot.HfApi')
    def test_fetch_hf_documents(self, mock_api):
        mock_api().hf_hub_download.return_value = 'test_path'
        result = fetch_hf_documents('test_repo', 'test_file')
        self.assertEqual(result, 'test_path')

if __name__ == '__main__':
    unittest.main()
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from huggingface_hub import HfApi, hf_hub_download, HfFolder
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv('.env')

app = Flask(__name__, static_folder='public')

def get_access_token():
    """Get the access token from environment variables."""
    return os.getenv('ACCESS_TOKEN')

def list_hf_repository_files(repo_id):
    """List all files in a specified Hugging Face Hub repository."""
    api = HfApi()
    folder = HfFolder()
    access_token = get_access_token()
    folder.save_token(access_token)
    available_docs = api.list_repo_files(repo_id)
    return available_docs
    
def select_document(docs):
    """Ask the user to select a document and return the selected document's name."""
    for idx, doc in enumerate(docs, start=1):
        print(f"{idx}. {doc}")
    selection = int(input("Select a document by number: ")) - 1
    return docs[selection]

def fetch_hf_documents(repo_id, filename):
    """Fetch a document from a Hugging Face Hub repository."""
    api = HfApi()
    file_path = hf_hub_download(repo_id=repo_id, filename=filename)
    return file_path

def load_and_process_document(file_path):
    """Load and process the selected .txt document."""
    loader = TextLoader(file_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
    return text_splitter.split_documents(documents)

vectordb = None
pdf_qa = None

chat_history = []

def chat():
    global pdf_qa, vectordb, chat_history

    user_input = request.json.get('message', '')
    
    # Initialize conversational Q&A chain with the vector store
    if pdf_qa is None:
        repo_id = 'asaurasieu'  # replace with your repo id
        available_docs = list_hf_repository_files(repo_id)
        selected_doc = select_document(available_docs)
        document_path = fetch_hf_documents(repo_id, selected_doc)
        document_chunks = load_and_process_document(document_path)
        
        # Initialize the vector store with embeddings from the selected document
        vectordb = Chroma.from_documents(document_chunks, embedding=OpenAIEmbeddings(), persist_directory="./data")
        vectordb.persist()
        
        pdf_qa = ConversationalRetrievalChain.from_llm(
            ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", max_tokens=4000),
            retriever=vectordb.as_retriever(search_kwargs={'k': 6}),
            return_source_documents=True,
            verbose=False
        )
        
    # Generate answer based on the selected document
    result = pdf_qa.invoke({"question": user_input, "chat_history": chat_history})
    chat_history.append((user_input, result["answer"]))  # Update chat history
    
    return jsonify({'response': result["answer"]})

 
if __name__ == "__main__":
    app.run(debug=True)
        

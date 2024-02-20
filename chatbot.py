import os
import sys
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv('.env')

def list_txt_documents(directory):
    """List all .txt documents in the specified directory."""
    return [file for file in os.listdir(directory) if file.endswith('.txt')]

def select_document(docs):
    """Ask the user to select a document and return the selected document's name."""
    for idx, doc in enumerate(docs, start=1):
        print(f"{idx}. {doc}")
    selection = int(input("Select a document by number: ")) - 1
    return docs[selection]

def load_and_process_document(file_path):
    """Load and process the selected .txt document."""
    loader = TextLoader(file_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
    return text_splitter.split_documents(documents)

# Directory where documents are stored
docs_folder = "./docs"

# Step 1: List and allow the user to select a .txt document
available_docs = list_txt_documents(docs_folder)
selected_doc = select_document(available_docs)
selected_doc_path = os.path.join(docs_folder, selected_doc)

# Step 2: Load and process the selected document
document_chunks = load_and_process_document(selected_doc_path)

# Step 3: Initialize the vector store with embeddings from the selected document
vectordb = Chroma.from_documents(document_chunks, embedding=OpenAIEmbeddings(), persist_directory="./data")
vectordb.persist()

# Initialize the conversational Q&A chain with the vector store
pdf_qa = ConversationalRetrievalChain.from_llm(
    ChatOpenAI(temperature=0.7, model_name='gpt-3.5-turbo', max_tokens=4000),
    retriever=vectordb.as_retriever(search_kwargs={'k': 6}),
    return_source_documents=True,
    verbose=False
)

# UI setup
yellow = "\033[0;33m"
green = "\033[0;32m"
white = "\033[0;39m"
chat_history = []

print(f"{yellow}---------------------------------------------------------------------------------")
print(f"Welcome to the Document Interaction Bot. Ready to interact with: {selected_doc}")
print('---------------------------------------------------------------------------------')

# Interaction loop
while True:
    query = input(f"{green}Prompt: ")
    if query.lower() in ["exit", "quit", "q", "f"]:
        print('Exiting')
        break
    if query == '':
        continue
    
    # Generate answer based on the selected document
    result = pdf_qa.invoke({"question": query, "chat_history": chat_history})
    print(f"{white}Answer: " + result["answer"])
    chat_history.append((query, result["answer"]))


import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage
from langchain_mistralai.chat_models import ChatMistralAI

# Initialize model and tokenizer for Mistral
model_name = "mistralai/Mistral-7B-Instruct-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
model.to("cuda")

# Initialize Chroma vector store
vectordb = Chroma(persist_directory="./data")

def generate_mistral_embeddings(text_chunks):
    embeddings = []
    for chunk in text_chunks:
        inputs = tokenizer(chunk, return_tensors="pt").to("cpu")
        with torch.no_grad():
            outputs = model(**inputs, output_hidden_states=True)
        chunk_embedding = outputs.hidden_states[-1].mean(dim=1).cpu().numpy()
        embeddings.append(chunk_embedding)
    return embeddings

# Index document chunks in Chroma
def index_document_chunks(chunks):
    embeddings = generate_mistral_embeddings(chunks)
    for chunk, embedding in zip(chunks, embeddings):
        vectordb.store(embedding.flatten(), chunk)

class ConversationalRetrievalChain:
    def __init__(self, vectordb):
        self.vectordb = vectordb
        self.history = []
    
    def update_history(self, user_query, model_response):
        self.history.append({"user": user_query, "model": model_response})

    def retrieve_relevant_chunks(self, query):
        relevant_chunks, _ = self.vectordb.retrieve(query, k=7)
        return relevant_chunks

def main():
    # Replace with docs
    document = "Your document text here."
    # Make the chunker
    chunks = chunk_document(document)
    index_document_chunks(chunks)

    retrieval_chain = ConversationalRetrievalChain(vectordb)

    while True:
        user_query = input("You: ")
        relevant_chunks = retrieval_chain.retrieve_relevant_chunks(user_query)

        model_response = "Generated response based on relevant chunks and the model's logic."
        print("Model:", model_response)

        retrieval_chain.update_history(user_query, model_response)

if __name__ == "__main__":
    main()

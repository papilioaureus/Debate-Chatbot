
import logging
import sys
import torch
import asyncio
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms.llama_cpp import LlamaCPP
from llama_index.llms.llama_cpp.llama_utils import (
    messages_to_prompt,
    completion_to_prompt,
)
from llama_index.core import ServiceContext
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index.embeddings.langchain import LangchainEmbedding


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

documents = SimpleDirectoryReader("content").load_data()

llm = LlamaCPP(
    # You can pass in the URL to a GGML model to download it automatically
    model_url='https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf',
    # optionally, you can set the path to a pre-downloaded model instead of model_url
    model_path=None,
    temperature=0.1,
    max_new_tokens=256,
    # llama2 has a context window of 4096 tokens, but we set it lower to allow for some wiggle room
    context_window=3900,
    # kwargs to pass to __call__()
    generate_kwargs={},
    # kwargs to pass to __init__()
    # set to at least 1 to use GPU
    model_kwargs={"n_gpu_layers": -1},
    # transform inputs into Llama2 format
    messages_to_prompt=messages_to_prompt,
    completion_to_prompt=completion_to_prompt,
    verbose=True,
)

embed_model = LangchainEmbedding(
  HuggingFaceEmbeddings(model_name="thenlper/gte-large")
)

service_context = ServiceContext.from_defaults(
    chunk_size=256,
    llm=llm,
    embed_model=embed_model
)

index = VectorStoreIndex.from_documents(documents, service_context=service_context)

query_engine = index.as_query_engine()
response = query_engine.query("The United States has traditionally regarded three regions as vital geopolitical centers, given their concentration of power and resources. Which ones?")
#Europe, East Asia and the Middle East.

print(response)

global conv_history  # Define conversation history as a global variable
conv_history = []

async def main(index):
    global conv_history  # Access the global conv_history variable
    while True:
        # Get user input for the query prompt
        new_query = input("Enter the new query prompt: ")
        if new_query == 'stop':
            break

        #add context
        context_and_query = "Here is the conversation history for context: " + str(conv_history) + " " + new_query

        # Use the new query prompt to generate a response
        query_engine = index.as_query_engine()
        response = query_engine.query(context_and_query)

        varr = 'USER: ' + new_query + '\nMISTRAL: ' + str(response)
        # Save the query-response pair in the conversation history
        conv_history.append(varr)
        print("Response:", response)

    # Print the conversation history after the loop breaks
    for entry in conv_history:
        print(entry)

# Run the event loop until the main coroutine is complete
asyncio.run(main(index))
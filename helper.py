from langchain_community.document_loaders import WebBaseLoader,PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings,HuggingFaceInferenceAPIEmbeddings
from chromadb.utils import embedding_functions
from langchain_chroma import Chroma
import bs4
import os
import shutil
import requests
from dotenv import load_dotenv
import streamlit as st
from chromadb.utils import embedding_functions
# import json
load_dotenv()
Gemini_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={os.environ['GEMINI']}"
# embedding = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
# embedding = HuggingFaceEmbeddings(model_name=r"D:\GenAI\RAG\Rag applicaiton-from medium tutoral\sentence-transformers\all-MiniLM-L6-v2")
model_name="sentence-transformers/all-MiniLM-L6-v2"
# embedding = HuggingFaceInferenceAPIEmbeddings(model_name=model_name,api_key=os.environ['HF_TOKEN'])
embedding = HuggingFaceInferenceAPIEmbeddings(
    api_key=os.environ['HF_TOKEN'], model_name=model_name
)
def get_response(query):
    """
    Get a response from the language model.

    Args:
        query (str): The input query.

    Returns:
        dict: The response from the language model.
    """
    return llm(query)

# @st.cache_resource
def load_documents(_url_file,_type='url|pdf'):
    """
    Load documents from a URL or PDF file.

    Args:
        _url_file (str): The URL or file path to load.
        _type (str, optional): The type of document to load ('url' or 'pdf'). Defaults to 'url|pdf'.

    Returns:
        list: The loaded documents.
    """
    if _type == 'pdf':
        print('\nLoading information from pdf')
        loader = PyPDFLoader(_url_file)
    else:
        print('\nLoading information from url')
        loader = WebBaseLoader(_url_file)

    document = loader.load()
    print('\nInformation Loaded')
    return document

# @st.cache_resource
def make_chunks(_document):
    """
    Split documents into chunks.

    Args:
        _document (list): The documents to split.

    Returns:
        list: The documents split into chunks.
    """
    print('\nCreating Chunks')
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 400,
        chunk_overlap = 100,
        length_function = len,
        add_start_index=True,)
    raw_chunks = text_splitter.split_documents(_document)
    print('\nChunks Created')
    return raw_chunks
# @st.cache_resource
def message_template(_msg,_type = 'ai|human'):
    """
    Create a message template for AI or human messages.

    Args:
        _msg (str): The message content.
        _type (str, optional): The type of message ('ai' or 'human'). Defaults to 'ai|human'.

    Returns:
        list: A list containing the message type, prefix, and content.
    """
    if _type=='ai':
         return [_type,'AI Response: ',_msg]
    elif _type=='human':
         return [_type,'Human Query: ',_msg]
# @st.cache_resource
def vector_store_chunks_retriver(_chunks):
    """
    Create a vector store from document chunks and return a retriever.

    Args:
        _chunks (list): The document chunks to store.

    Returns:
        Retriever: A retriever for the vector store.
    """
    # print('\n')

    # if os.path.exists('chroma'):
    #     shutil.rmtree('chroma')

    print('\nCreating vector store')
    vector_store = Chroma.from_documents(documents=_chunks,embedding=embedding)
                                        
    print('\nVector Store Created. Saving Vector Store and Returning Retriever')
    return vector_store.as_retriever(search_type="mmr",search_kwargs={"k":3})

# @st.cache_resource
def get_prompt(_question,_context):
    """
    Generate a prompt for question-answering tasks.

    Args:
        _question (str): The question to be answered.
        _context (str): The context for answering the question.

    Returns:
        str: The generated prompt.
    """
    prompt = f"""
    You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

Question: {_question} 

Context: {_context} 

Answer:"""
    return prompt
# @st.cache_resource
def llm(_payload):
    """
    Send a request to the language model API and get the response.

    Args:
        _payload (dict): The payload to send to the API.

    Returns:
        dict: The JSON response from the API.
    """
    # response = requests.post(API_URL, headers=headers json=payload)
    response = requests.post(Gemini_API_URL, json=_payload)
    print("\nAugmenting Information... Please Wait")  
    return response.json()
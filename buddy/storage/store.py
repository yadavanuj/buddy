import os
import hashlib
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from .elseify import get_synonyms, split_identifier
from langchain_chroma import Chroma
from langchain_core.documents import Document
from getpass import getpass
from langchain_community.vectorstores.utils import filter_complex_metadata
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY=os.getenv("GEMINI_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)

# DB
vector_store = Chroma(collection_name="call_graph", embedding_function=embedding_function, persist_directory="./buddy_db")

def generate_md5(function_name: str) -> str:
    return hashlib.md5(function_name.encode()).hexdigest()

def process_function_name(name):
    words = split_identifier(name)
    synonyms = {w: get_synonyms(w) for w in words}
    
    return list(set(synonyms))

def store_function_in_chroma(function_name, file_path, call_relations):
    """Store function metadata in ChromaDB using LangChain."""
    
    # Get function synonyms
    synonyms = process_function_name(function_name)
    
    # Generate NL description
    nl_description = (
        f"Function `{function_name}` is located in `{file_path}`. "
        f"It interacts with {', '.join(call_relations)}. "
        f"Possible synonyms: {', '.join(synonyms)}."
    )

    # Create LangChain document
    function_id = generate_md5(function_name)
    doc = Document(
        id=function_id,
        page_content=nl_description,
        metadata={
            "function": function_name,
            "file": file_path,
            "calls": call_relations,
            "synonyms": synonyms
        }
    )

    # Filter out complex metadata
    filtered_documents = filter_complex_metadata([doc])

    # Add to ChromaDB
    vector_store.add_documents(filtered_documents)

# Example Usage:
# store_function_in_chroma("fetchUserData", "src/utils.js", ["parseResponse", "handleError"])

def search_function_in_chroma(nl_query, top_k=5):
    """Search functions based on a natural language query."""
    
    results = vector_store.similarity_search(nl_query, k=top_k)
    
    return [(res.page_content, res.metadata) for res in results]

def save_call_graph(call_graph):
    for function in call_graph.nodes:
        file_path = call_graph.nodes[function]["file_path"]
        call_relations = list(call_graph.successors(function))
    
        store_function_in_chroma(function, file_path, call_relations)

def search_function_in_chroma(nl_query, top_k=5):
    """Search functions based on a natural language query."""
    
    results = vector_store.similarity_search(nl_query, k=top_k)
    
    return [(res.page_content, res.metadata) for res in results]

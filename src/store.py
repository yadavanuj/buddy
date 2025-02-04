import os
import google.generativeai as genai
from langchain.embeddings import GoogleGenerativeAIEmbeddings

GOOGLE_API_KEY=os.getenv("GEMINI_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


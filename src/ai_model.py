import os
import google.generativeai as genai

GOOGLE_API_KEY=os.getenv("GEMINI_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

ai_model = genai.GenerativeModel('gemini-1.5-flash')


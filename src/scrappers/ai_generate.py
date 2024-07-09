import google.generativeai as genai
import os

def generate(query):
    genai.configure(api_key=os.getenv('API_KEY'))
    model = genai.GenerativeModel('gemini-1.0-pro-latest')
    response = model.generate_content(f"{query} with code example")
    return response.text

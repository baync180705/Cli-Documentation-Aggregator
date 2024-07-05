import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv('API_KEY'))
user_input = input("what would u like to search... ")
model = genai.GenerativeModel('gemini-1.0-pro-latest')
response = model.generate_content(f"{user_input} with code example")
print(response.text)
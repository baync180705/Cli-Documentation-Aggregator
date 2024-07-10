import google.generativeai as genai
import os

#defining a generate function to generate ai generated output
def generate(query):
    genai.configure(api_key=os.getenv('API_KEY')) #configuring using api key
    model = genai.GenerativeModel('gemini-1.0-pro-latest') #selecting the desired model
    response = model.generate_content(f"{query} with code example") #prompting the model using user input
    return response.text #returning response text for output

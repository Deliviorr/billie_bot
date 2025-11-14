import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_antwoord(prompt):
    model = genai.GenerativeModel(os.getenv("MODEL_VERSIE"))
    response = model.generate_content(prompt)
    return response.text

#data tracking codes 
df = pd.read_csv('tracking_codes.csv')

# krijg track code

#output track data

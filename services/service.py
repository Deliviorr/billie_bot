import google.generativeai as genai
# from config.config import GEMINI_API_KEY, MODEL_VERSIE
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_antwoord(prompt):
    model = genai.GenerativeModel(os.getenv("MODEL_VERSIE"))
    response = model.generate_content(prompt)
    print(response.text)
    return response.text

get_antwoord("Leg uit wat ai is in 1 zin")

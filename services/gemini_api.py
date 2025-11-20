from google import genai
from google.genai import types
import time
from dotenv import load_dotenv
from services.database import create_case
import os

load_dotenv()

client = genai.Client()

# Create the File Search store
file_search_store = client.file_search_stores.create(
    config={'display_name': 'billie-bot'}
)

# Upload and import a file into the File Search store
operation = client.file_search_stores.upload_to_file_search_store(
    file='FAQ.txt',
    file_search_store_name=file_search_store.name,
    config={
        'display_name': 'display-file-name',
    }
)

# Wait until import is complete
while not operation.done:
    time.sleep(2)
    operation = client.operations.get(operation)

# Correct File Search tool syntax
tool = types.Tool(
    file_search=types.FileSearch(
        file_search_store_names=[file_search_store.name]
    )
)

def get_antwoord(vraag):
    system_prompt = f"""
Je bent Billie, een vriendelijke klantenservice chatbot.

Regels:
- Als je het antwoord 100% zeker weet → geef het direct.
- Als de vraag complex is, buiten je kennis ligt, of een menselijke medewerker nodig heeft → begin je antwoord met precies deze tag:
  CASE_NODIG
- Als case nodig is, hou de worden dan onder 255 karakters, zodat het past in de database

Voorbeelden van CASE_NODIG:
- Terugbetaling buiten termijn
- Kapot product of klacht
- Vraag over een specifiek order
- Accountproblemen, inloggen, wachtwoord, etc.

Vraag van de klant:
{vraag}
"""

    try:
        response = client.models.generate_content(
            model=os.getenv("MODEL_VERSIE"),
            contents=system_prompt + vraag,
            config=types.GenerateContentConfig(
            tools=[tool]
            )
        )
        
        gemini_text = response.text.strip()

        if gemini_text.upper().startswith("CASE_NODIG"):
            clean_answer = gemini_text[10:].strip() 

            if not clean_answer:
                clean_answer = "Deze vraag is te complex voor mij. Ik maak een case aan voor een medewerker."

            case_id = create_case(customer_question=vraag, gemini_answer=gemini_text)

            return f"{clean_answer}\n\n" \
                   f"Ik heb een case voor je aangemaakt: **{case_id}**\n" \
                   f"Een medewerker neemt binnen 24 uur contact met je op via e-mail. Bedankt voor je geduld!"

        else:
            return gemini_text

    except Exception as e:
        return "Sorry, er is iets misgegaan. Probeer het later opnieuw"
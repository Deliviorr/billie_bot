from google import genai
from google.genai import types
import time
from dotenv import load_dotenv

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
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""Je bent een klantenservice chatbot, beantwoord de vraag van de klant vriendelijk en duidelijk. Als de vraag
        niet in de data staat, suggereer dan of je een case moet aanmaken, zodat de klantenservice medewerker het gemakkelijk kan oppakken
        
        Vraag van klant:
        {vraag}""",
        config=types.GenerateContentConfig(
            tools=[tool]
        )
    )

    return response.text
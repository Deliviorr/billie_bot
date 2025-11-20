import streamlit as st
from services.gemini_api import get_antwoord

# Initialiseer session state voor berichten (als het nog niet bestaat)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Toon de chatgeschiedenis
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input aan de bottom (automatisch sticky)
if prompt := st.chat_input("Type je vraag:"):
    # Voeg user-bericht toe
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Genereer en voeg assistant-bericht toe
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = get_antwoord(prompt)  # Jouw functie voor het antwoord
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Waarschuwing voor lege prompt (optioneel, maar chat_input negeert lege inputs)
    if not prompt.strip():
        st.warning("Type eerst een bericht")
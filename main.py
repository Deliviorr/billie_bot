import streamlit as st
from services.service import get_antwoord

st.set_page_config(page_title="Billie Bot", layout='centered')

st.title("Billie Chat")

prompt = st.text_input("Type je vraag: ")

if st.button("Verstuur"):
    if prompt.strip():
        st.write("**Jij:**", prompt)
        response = get_antwoord(prompt)
        st.write(f"**Billie:** {response}")
    else:
        st.warning("Type eerst een bericht")

import streamlit as st
from services.gemini_api import get_antwoord
from datetime import datetime

BOL_BLUE = "#1A7EF8"
BOL_YELLOW = "#FFD200"
BG_LIGHT = "#F5F7FA"

st.set_page_config(page_title="Billie Bot ", layout="wide")

st.markdown(
    f"""
    <style>
    
    /* ---- FIX: volledige pagina wit ---- */
    html, body, .stApp {{
        background-color: #FFFFFF !important;
    }}
    
    .page-bg {{
        background-color: {BG_LIGHT};
        padding: 16px;
    }}
    .bubble-user {{
        background: #F0F0F0;
        border: 1px solid #D0D0D0;
        border-radius: 12px;
        padding: 10px 14px;
        max-width: 70%;
        word-wrap: break-word;
    }}
    .bubble-assistant {{
        background: #1A7EF8;
        color: white;
        border: 1px solid #005BCE;
        border-radius: 12px;
        padding: 10px 14px;
        max-width: 70%;
        word-wrap: break-word;
    }}
    .timestamp {{
        font-size: 11px;
        color: #666;
        margin-top: 6px;
    }}
    .title {{
        font-size: 28px;
        font-weight: 800;
        color: {BOL_BLUE};
        margin-bottom: 6px;
    }}
    .subtitle {{
        font-size: 14px;
        color: #003DA5;
        margin-bottom: 18px;
    }}
    </style>
    <div class="page-bg">
        <div class="title">Billie Bot</div>
        <div class="subtitle">Stel je vraag en krijg direct antwoord</div>
    </div>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []

def render_chat():
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            role = msg.get("role", "assistant")
            content = msg["content"]
            ts = msg.get("ts", "")
            ts_html = f'<div class="timestamp">{ts}</div>' if ts else ""

            if role == "user":
                col_l, col_r = st.columns([1, 3])
                with col_l:
                    st.write("")
                with col_r:
                    st.markdown(f'<div class="bubble-user">{content}</div>', unsafe_allow_html=True)
                    st.markdown(ts_html, unsafe_allow_html=True)

            else:  # assistant
                col_l, col_r = st.columns([3, 1])
                with col_l:
                    st.markdown(f'<div class="bubble-assistant">{content}</div>', unsafe_allow_html=True)
                    st.markdown(ts_html, unsafe_allow_html=True)
                with col_r:
                    st.write("")

render_chat()

prompt = st.chat_input("Type je vraag:")

if prompt is not None:
    if not prompt.strip():
        st.warning("Typ eerst een bericht")
    else:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "ts": ts
        })

        try:
            answer = get_antwoord(prompt)
            if answer is None:
                answer = "Geen antwoord ontvangen."
        except Exception as e:
            answer = f"Fout bij ophalen van antwoord: {e}"

        ts2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "ts": ts2
        })
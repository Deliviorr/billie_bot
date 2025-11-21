import streamlit as st
import pandas as pd
from services.database import connect_db

BOL_BLUE = "#1A7EF8"
BOL_YELLOW = "#FFD200"
BG_LIGHT = "#F5F7FA"

# Page config
st.set_page_config(page_title="Case Dashboard", layout="wide")

# Custom CSS
st.markdown(
    f"""
    <style>
        body, .stApp {{
            background-color: {BG_LIGHT};
        }}

        .main-header {{
            background: white;
            padding: 24px;
            border-radius: 16px;
            border-left: 6px solid {BOL_BLUE};
            margin-bottom: 20px;
        }}
        .main-header h1 {{
            color: {BOL_BLUE};
            margin: 0;
            font-size: 32px;
            font-weight: 800;
        }}
        .main-header p {{
            color: #003DA5;
            margin-top: 6px;
            font-size: 15px;
        }}

        .case-card {{
            background: white;
            padding: 18px;
            border-radius: 16px;
            border: 1px solid #E5E7EB;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }}

        .case-title {{
            color: {BOL_BLUE};
            font-weight: 700;
            font-size: 20px;
            margin-bottom: 6px;
        }}

        .case-label {{
            color: #666;
            font-size: 13px;
            margin-bottom: -4px;
        }}

        .case-value {{
            font-size: 15px;
            font-weight: 600;
            margin-bottom: 10px;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---- HEADER ----
st.markdown(
    """
    <div class="main-header">
        <h1>Case Dashboard</h1>
        <p>Bekijk alle cases direct vanuit de database</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---- DATABASE ----
conn = connect_db()
cur = conn.cursor()

query = '''
    SELECT *
    FROM cases
'''

cur.execute(query)
rows = cur.fetchall()

col_names = [desc[0] for desc in cur.description]
df = pd.DataFrame(rows, columns=col_names)

case_id_column = "case_id"   # <--- vaste kolomnaam

zoek_id = st.text_input(
    "Zoek een Case ID",
    placeholder="Typ een Case ID...",
)

# Case-insensitive search + automatische cast naar string
if zoek_id.strip():
    zoekwaarde = zoek_id.strip().lower()
    df = df[df[case_id_column].astype(str).str.lower().str.contains(zoekwaarde)]

num_cols = 3 

# Loop in blokjes van 3
for i in range(0, len(df), num_cols):

    row_slice = df.iloc[i:i+num_cols]
    cols = st.columns(num_cols)

    for col, (_, row) in zip(cols, row_slice.iterrows()):
        with col:
            st.markdown("<div class='case-card'>", unsafe_allow_html=True)

            titel = row[col_names[0]]
            st.markdown(f"<div class='case-title'>{titel}</div>", unsafe_allow_html=True)

            for col_name in col_names[1:]:
                st.markdown(f"<div class='case-label'>{col_name}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='case-value'>{row[col_name]}</div>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
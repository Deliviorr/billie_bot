import streamlit as st
import pandas as pd
from services.database import connect_db

conn = connect_db()
cur = conn.cursor()

query = '''
    SELECT *
    FROM cases
'''

cur.execute(query)
rows = cur.fetchall()

col_names = []

for desc in cur.description:
    col_names.append(desc[0])

df = pd.DataFrame(rows, columns=col_names)
st.dataframe(df)
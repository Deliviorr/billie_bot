import os
import psycopg2
from psycopg2.extras import RealDictCursor
import uuid
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")  

def connect_db():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn

def generate_case_id():
    return "CASE-" + str(uuid.uuid4())[:8].upper()

def create_case(customer_question: str, gemini_answer: str) -> str:
    case_id = generate_case_id()
    
    sql = """
    INSERT INTO cases (case_id, customer_question, gemini_answer)
    VALUES (%s, %s, %s)
    RETURNING case_id
    """
    
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(sql, (case_id, customer_question, gemini_answer))
        conn.commit()
        cur.close()
        conn.close()
        return case_id
    except Exception as e:
        print(f"Database fout bij aanmaken case: {e}")

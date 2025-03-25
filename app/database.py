import sqlite3
from datetime import datetime

DB_PATH = "logs/chatbot_logs.db"

# ✅ Create Table (Run Once)
def create_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chatbot_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        question TEXT,
        context_snippet TEXT,
        response TEXT,
        response_time REAL,
        confidence_score REAL,
        bleu_score REAL,
        rouge_score REAL
    );
    """)
    conn.commit()
    conn.close()

# ✅ Insert Data into Database
def insert_log(question, context, response, response_time, confidence, bleu, rouge):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()

    cursor.execute("""
    INSERT INTO chatbot_logs (timestamp, question, context_snippet, response, response_time, confidence_score, bleu_score, rouge_score)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, (timestamp, question, context, response, response_time, confidence, bleu, rouge))

    conn.commit()
    conn.close()

# ✅ Run this file once to create the table
if __name__ == "__main__":
    create_table()
    print("✅ Database initialized successfully!")

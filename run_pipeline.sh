#!/bin/bash
cd /Users/jureddy/chatbot_rag_pipeline

export PATH="/opt/anaconda3/bin:$PATH"

echo "🔁 Starting Chatbot Pipeline at $(date)"

/opt/anaconda3/bin/python3 app/database.py
/opt/anaconda3/bin/python3 app/chatbot_runner.py

echo "✅ Pipeline Finished at $(date)"


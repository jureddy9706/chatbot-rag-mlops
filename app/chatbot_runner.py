import time
import torch
import sqlite3
from sentence_transformers import SentenceTransformer
from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
import chromadb
from evaluate_metrics import calculate_bleu, calculate_rouge
from database import insert_log
from utils import truncate_context, load_questions

# ✅ Load models
device = "cuda" if torch.cuda.is_available() else "cpu"
embedding_model = SentenceTransformer("all-MiniLM-L6-v2", device=device)
chroma_client = chromadb.PersistentClient(path="./chroma_db")  # Ensure this path exists
collection = chroma_client.get_collection(name="unh_programs")
llm = OllamaLLM(model="mistral")

# ✅ Define chatbot function
def answer_query(query, top_k=3, max_context_words=600):
    start_time = time.time()
    
    query_embedding = embedding_model.encode(query).tolist()
    
    # 🔍 Search ChromaDB for relevant context
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    retrieved_docs = results["documents"][0] if results["documents"] else []
    context = truncate_context(retrieved_docs, max_words=max_context_words)

    # 📝 Generate response using Mistral
    prompt_template = """You are a university assistant. Answer only using the provided context.
    
    Context:
    {context}
    
    Question:
    {question}
    
    Answer:"""
    prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)
    full_prompt = prompt.format(context=context, question=query)
    
    response = llm.invoke(full_prompt)
    response_time = round(time.time() - start_time, 3)

    # 📊 Evaluate Performance
    confidence_score = min(1.0, len(context.split()) / max_context_words)  # Simple confidence metric
    bleu = calculate_bleu(context, response)
    rouge = calculate_rouge(context, response)

    # ✅ Store in Database
    insert_log(query, context[:300], response, response_time, confidence_score, bleu, rouge)

    return response

# ✅ Run batch processing from file
if __name__ == "__main__":
    questions = load_questions("questions_list.txt")
    for q in questions:
        print(f"🔹 Q: {q}")
        ans = answer_query(q)
        print(f"💬 A: {ans}\n{'-'*60}")

from utils import get_context_from_chromadb
from database import get_answer_from_llm  # This is your Ollama call

def get_response(question):
    context = get_context_from_chromadb(question)
    answer = get_answer_from_llm(question, context)
    return answer


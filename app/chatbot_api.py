from fastapi import FastAPI, Request
from chatbot_runner import get_response  # use your existing logic

app = FastAPI()

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    question = data.get("question", "")
    answer = get_response(question)  # assuming this function returns answer string
    return {"answer": answer}


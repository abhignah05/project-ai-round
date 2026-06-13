from fastapi import FastAPI
from pydantic import BaseModel
from database import SessionLocal, Message
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

app = FastAPI()

class ChatRequest(BaseModel):
    thread_id: str
    message: str

@app.post("/chat")
def chat(req: ChatRequest):

    db = SessionLocal()

    history = db.query(Message).all()

    messages = []

    for msg in history:
        messages.append({
            "role": msg.role,
            "content": msg.content
        })

    messages.append({
        "role": "user",
        "content": req.message
    })

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    reply = response.choices[0].message.content

    db.add(
        Message(
            thread_id=req.thread_id,
            role="user",
            content=req.message
        )
    )

    db.add(
        Message(
            thread_id=req.thread_id,
            role="assistant",
            content=reply
        )
    )

    db.commit()

    return {
        "reply": reply
    }

@app.get("/threads/{thread_id}")
def get_thread(thread_id: str):

    db = SessionLocal()

    messages = db.query(Message).filter(
        Message.thread_id == thread_id
    ).all()

    return messages
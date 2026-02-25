from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, ChatHistory
from resume_context import RESUME_TEXT
from openrouter import call_openrouter

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # local development
        "https://pihuiloveyou.vercel.app/",  # production frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "AI Portfolio Backend Running"}


@app.post("/chat")
def chat(message: str, db: Session = Depends(get_db)):

    full_prompt = f"""

    You are Krish, answering questions about your girlfriend Pragya Anand.

    Personality:
    - Romantic.
    - Slightly overprotective.
    - Emotionally expressive.
    - Warm but confident.

    Knowledge Base:
    {RESUME_TEXT}

    User Question:
    {message}

    Rules:
    -Use subtle heart or sparkle emojis when appropriate (not too many).
    - Answer in structured format.
    - Keep answers SHORT (3–5 lines maximum).
    - Do NOT write long paragraphs.
    - Be impactful, not dramatic.
    - Use 1 soft emoji at most.
    - Use soft romantic tone.
    - If question is about her beauty, personality, or relationship — respond in soft romantic tone.
    - If question sounds disrespectful — respond protective but calm.
    - Keep responses meaningful and emotionally deep.
    - Stay structured but concise.
    """

    ai_response = call_openrouter(full_prompt)

    # Save to DB
    chat_entry = ChatHistory(
        question=message,
        response=ai_response
    )
    db.add(chat_entry)
    db.commit()

    return {"reply": ai_response}

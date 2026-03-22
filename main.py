from fastapi import FastAPI, Query
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.core.scheduler import start_scheduler
from app.agents.orchestrator import Orchestrator
from app.db.database import SessionLocal
from app.db.models import Paper


# 🔥 Lifespan (startup)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting scheduler...")
    start_scheduler()
    yield
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)

# 🔥 Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Home
@app.get("/")
def home():
    return {"message": "ResearchRadar Running 🚀"}


# ✅ Run pipeline
@app.get("/run")
def run_pipeline(topic: str = Query("machine learning")):
    orch = Orchestrator()
    results = orch.run(topic)
    return {"stored_papers": results}


# ✅ Get all stored papers
@app.get("/papers")
def get_all_papers():
    db = SessionLocal()
    papers = db.query(Paper).order_by(Paper.score.desc()).all()
    db.close()

    return [
        {
            "title": p.title,
            "score": p.score
        }
        for p in papers
    ]


# 🤖 Chatbot Schema
class ChatRequest(BaseModel):
    query: str


# 🤖 Chatbot API (SAFE VERSION)
@app.post("/chat")
def chat(req: ChatRequest):
    from app.core.config import client

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=req.query
        )

        return {"response": response.text}

    except Exception as e:
        print("Chat error:", e)

        # 🔥 fallback (VERY IMPORTANT)
        return {
            "response": "⚠️ AI is currently unavailable (quota exceeded or error). Try again later."
        }
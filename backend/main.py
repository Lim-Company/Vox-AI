from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .routers import calls, messages, appointments, summaries, messages_api

from .models import Base              # SQLAlchemy Base from models.py
from .db import engine                # SQLAlchemy engine from db.py

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    print("✔️ Database tables created")

    yield

    # Shutdown
    print("👋 API shutting down")

app = FastAPI(
    title="AI Secretary API",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(calls.router)
app.include_router(messages.router)
app.include_router(appointments.router)
app.include_router(summaries.router)
app.include_router(messages_api.router)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

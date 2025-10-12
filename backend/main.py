from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import calls, messages, appointments, summaries

app = FastAPI(title="AI Secretary API", version="0.1.0")

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

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

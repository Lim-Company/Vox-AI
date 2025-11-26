from fastapi import Header, HTTPException
from typing import Generator

# SQLAlchemy session provider
from .db import SessionLocal
from .db import settings
from sqlalchemy.orm import Session


async def verify_webhook(x_webhook_secret: str = Header(default=None)):
    # Allow everything on local (your laptop) if you want:
    if settings.ENV == "local":
        return

    # In dev/test/prod → enforce secret
    expected = settings.WEBHOOK_SECRET

    if not x_webhook_secret or x_webhook_secret != expected:
        raise HTTPException(
            status_code=401,
            detail="Invalid webhook signature",
        )


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

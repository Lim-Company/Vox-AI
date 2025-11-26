from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class MessageIn(BaseModel):
    client_id: str
    from_number: str
    to_number: str
    body: str

class MessageOut(MessageIn):
    id: int
    received_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CallEvent(BaseModel):
    client_id: str
    call_id: str
    from_number: str
    to_number: str
    status: str = Field(description="ringing|in-progress|completed|failed")
    recording_url: Optional[str] = None

class Appointment(BaseModel):
    client_id: str
    title: str
    starts_at: datetime
    ends_at: datetime
    location: Optional[str] = None
    notes: Optional[str] = None

class SummaryRequest(BaseModel):
    client_id: str
    transcript: str

class SummaryOut(BaseModel):
    client_id: str
    bullets: List[str]
    action_items: List[str] = []

# ------------------------------------------
# SQLAlchemy Models (Actual DB Tables)
# ------------------------------------------

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, Text, func

class Base(DeclarativeBase):
    pass

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    client_id: Mapped[str] = mapped_column(String(50), nullable=False)
    from_number: Mapped[str] = mapped_column(String(30), nullable=False)
    to_number: Mapped[str] = mapped_column(String(30), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
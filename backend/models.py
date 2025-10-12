from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class MessageIn(BaseModel):
    client_id: str
    from_number: str
    to_number: str
    body: str

class MessageOut(MessageIn):
    id: str
    received_at: datetime

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

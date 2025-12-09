# backend/schemas/calls.py

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


# ---------- Call Segment Schemas ----------

class CallSegmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    call_id: UUID
    speaker: str
    transcript_text: str
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    created_at: datetime


# ---------- Call Summary Schemas ----------

class CallSummaryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    call_id: UUID
    summary_text: str
    primary_intent: Optional[str] = None
    urgency: Optional[str] = None
    # This matches next_actions: list | None in the SQLAlchemy model
    next_actions: Optional[list] = None
    raw_llm_response: Optional[dict] = None
    created_at: datetime
    updated_at: datetime


# ---------- Call Schemas ----------

class CallRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    external_id: Optional[str] = None
    from_number: str
    to_number: str
    status: str
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    created_at: datetime
    updated_at: datetime


class CallListItem(CallRead):
    """
    What you return in GET /api/v1/calls listing.
    For now, it's the same as CallRead.
    """
    pass


class CallDetailRead(CallRead):
    """
    Full call detail: base call fields + segments + summary.
    Used by Call Detail page in the dashboard.
    """
    segments: List[CallSegmentRead] = []
    summary: Optional[CallSummaryRead] = None

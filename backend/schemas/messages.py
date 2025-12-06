from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class MessageIn(BaseModel):
    client_id: Optional[str] = None
    from_number: str
    to_number: str
    body: str


class MessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    client_id: Optional[str] = None
    from_number: str
    to_number: str
    body: str
    created_at: datetime

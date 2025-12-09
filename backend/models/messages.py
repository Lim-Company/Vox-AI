from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import declarative_mixin

from backend.db import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    client_id = Column(String(64), nullable=True, index=True)

    from_number = Column(String(32), nullable=False, index=True)
    to_number = Column(String(32), nullable=False, index=True)

    body = Column(Text, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )

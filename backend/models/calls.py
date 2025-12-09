import uuid
from datetime import datetime
from typing import Optional, List

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Integer,
    Text,
    ForeignKey,
    JSON,
    func,
)
from sqlalchemy.orm import relationship

from backend.db import Base


def _uuid_str() -> str:
    """Generate a UUID string for SQLite-friendly primary keys."""
    return str(uuid.uuid4())


class Call(Base):
    __tablename__ = "calls"

    # Use String PK instead of Postgres UUID type so SQLite is happy
    id = Column(String(36), primary_key=True, default=_uuid_str)

    external_id = Column(String(100), unique=True, index=True, nullable=True)
    from_number = Column(String(32), index=True, nullable=False)
    to_number = Column(String(32), index=True, nullable=False)

    status = Column(
        String(32),
        default="incoming",
        index=True,
        nullable=False,
    )

    started_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=True,
    )
    ended_at = Column(DateTime(timezone=True), nullable=True)

    duration_seconds = Column(Integer, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    segments = relationship(
        "CallSegment",
        back_populates="call",
        cascade="all, delete-orphan",
        order_by="CallSegment.started_at",
    )

    summary = relationship(
        "CallSummary",
        back_populates="call",
        uselist=False,
        cascade="all, delete-orphan",
    )


class CallSegment(Base):
    __tablename__ = "call_segments"

    id = Column(String(36), primary_key=True, default=_uuid_str)

    call_id = Column(
        String(36),
        ForeignKey("calls.id", ondelete="CASCADE"),
        nullable=False,
    )

    speaker = Column(String(32), nullable=False, index=True)

    started_at = Column(DateTime(timezone=True), nullable=True)
    ended_at = Column(DateTime(timezone=True), nullable=True)

    transcript_text = Column(Text, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    call = relationship("Call", back_populates="segments")


class CallSummary(Base):
    __tablename__ = "call_summaries"

    id = Column(String(36), primary_key=True, default=_uuid_str)

    call_id = Column(
        String(36),
        ForeignKey("calls.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    summary_text = Column(Text, nullable=False)
    primary_intent = Column(String(128), nullable=True)
    urgency = Column(String(32), nullable=True)

    # SQLAlchemy's generic JSON type works on SQLite (it stores as TEXT under the hood)
    next_actions = Column(JSON, nullable=True)
    raw_llm_response = Column(JSON, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    call = relationship("Call", back_populates="summary")

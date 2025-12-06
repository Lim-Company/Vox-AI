import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Integer,
    Text,
    ForeignKey,
    JSON,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from backend.db import Base  # your Base import may be backend.db.Base


class Call(Base):
    __tablename__ = "calls"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    external_id: Mapped[str | None] = mapped_column(String(100), unique=True, index=True)
    from_number: Mapped[str] = mapped_column(String(32), index=True)
    to_number: Mapped[str] = mapped_column(String(32), index=True)

    status: Mapped[str] = mapped_column(
        String(32),
        default="incoming",
        index=True,
        nullable=False,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    duration_seconds: Mapped[int | None] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
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

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    call_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("calls.id", ondelete="CASCADE"), nullable=False
    )

    speaker: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    transcript_text: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    call = relationship("Call", back_populates="segments")


class CallSummary(Base):
    __tablename__ = "call_summaries"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    call_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("calls.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    summary_text: Mapped[str] = mapped_column(Text, nullable=False)
    primary_intent: Mapped[str | None] = mapped_column(String(128))
    urgency: Mapped[str | None] = mapped_column(String(32))
    next_actions: Mapped[list | None] = mapped_column(JSON)
    raw_llm_response: Mapped[dict | None] = mapped_column(JSON)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    call = relationship("Call", back_populates="summary")

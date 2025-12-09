# backend/models/__init__.py

"""
Central export point for SQLAlchemy models.
"""

from backend.db import Base  # declarative Base

# Import model classes so they're registered on Base.metadata
from .messages import Message
from .calls import Call, CallSegment, CallSummary

__all__ = [
    "Message",
    "Call",
    "CallSegment",
    "CallSummary",
]

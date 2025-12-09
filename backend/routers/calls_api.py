from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..deps import get_db
from ..models.calls import Call, CallSegment, CallSummary
from ..schemas.calls import (
    CallListItem,
    CallDetailRead,
)

router = APIRouter(
    prefix="/api/v1/calls",
    tags=["calls"],
)


@router.get("", response_model=List[CallListItem])
def list_calls(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    """
    List calls in descending order (newest first).
    """
    calls = (
        db.query(Call)
        .order_by(Call.started_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return calls


@router.get("/{call_id}", response_model=CallDetailRead)
def get_call_detail(
    call_id: str,
    db: Session = Depends(get_db),
):
    """
    Return the call, its segments, and its summary.
    """
    call = db.get(Call, call_id)
    if not call:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Call not found",
        )

    return call

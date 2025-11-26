from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..deps import get_db
from ..models import Message as DBMessage, MessageOut

router = APIRouter(
    prefix="/api/v1/messages",
    tags=["messages"],
)


@router.get(
    "",
    response_model=List[MessageOut],
)
def list_messages(
    client_id: Optional[str] = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> List[MessageOut]:
    """
    List messages, optionally filtered by client_id, with simple pagination.
    """
    query = db.query(DBMessage)

    if client_id:
        query = query.filter(DBMessage.client_id == client_id)

    messages = (
        query.order_by(DBMessage.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return messages


@router.get(
    "/{message_id}",
    response_model=MessageOut,
)
def get_message(
    message_id: int,
    db: Session = Depends(get_db),
) -> MessageOut:
    """
    Fetch a single message by its ID.
    """
    msg = db.get(DBMessage, message_id)
    if not msg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )
    return msg

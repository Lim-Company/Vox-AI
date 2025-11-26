from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from ..models import MessageIn, MessageOut, Message as DBMessage
from ..deps import verify_webhook, get_db

router = APIRouter(
    prefix="/webhook/messages",
    tags=["messages"]
)

@router.post(
    "",
    response_model=MessageOut,
    dependencies=[Depends(verify_webhook)]
)

async def receive_message(
    msg: MessageIn,
    db: Session = Depends(get_db)
):

    """
    Receives a webhook message (e.g., from Twilio) and stores it in the DB.
    """

    # Create DB object
    db_msg = DBMessage(
        client_id=msg.client_id,
        from_number=msg.from_number,
        to_number=msg.to_number,
        body=msg.body
    )

    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)

    # Convert SQLAlchemy model -> Pydantic MessageOut

    return MessageOut(
        id=db_msg.id,
        received_at=datetime.utcnow(),
        **msg.model_dump()
    )

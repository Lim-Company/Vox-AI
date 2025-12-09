from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..deps import verify_webhook, get_db
from ..models.messages import Message as DBMessage
from ..schemas.messages import MessageIn, MessageOut

router = APIRouter(
    prefix="/webhook/messages",
    tags=["messages"],
)


@router.post(
    "",
    response_model=MessageOut,
    dependencies=[Depends(verify_webhook)],
)
async def receive_message(
    msg: MessageIn,
    db: Session = Depends(get_db),
):
    """
    Receives a webhook message (e.g., from Twilio) and stores it in the DB.
    """

    db_msg = DBMessage(
        client_id=msg.client_id,
        from_number=msg.from_number,
        to_number=msg.to_number,
        body=msg.body,
    )

    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)

    # Build MessageOut explicitly (since MessageOut expects received_at)
    return MessageOut(
        id=db_msg.id,
        client_id=db_msg.client_id,
        from_number=db_msg.from_number,
        to_number=db_msg.to_number,
        body=db_msg.body,
        received_at=datetime.utcnow(),
    )

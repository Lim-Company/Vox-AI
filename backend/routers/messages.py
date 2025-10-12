from fastapi import APIRouter, Depends
from ..models import MessageIn, MessageOut
from ..deps import verify_webhook
from datetime import datetime
import uuid

router = APIRouter(prefix="/webhook/messages", tags=["messages"])

@router.post("", response_model=MessageOut, dependencies=[Depends(verify_webhook)])
async def receive_message(msg: MessageIn):
    # TODO: persist to DB
    return MessageOut(id=str(uuid.uuid4()), received_at=datetime.utcnow(), **msg.model_dump())

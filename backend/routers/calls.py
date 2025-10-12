from fastapi import APIRouter, Depends
from ..models import CallEvent
from ..deps import verify_webhook

router = APIRouter(prefix="/webhook/calls", tags=["calls"])

@router.post("", dependencies=[Depends(verify_webhook)])
async def receive_call_event(event: CallEvent):
    # TODO: persist event, trigger transcription job if completed+recording_url
    return {"ok": True, "received": event.model_dump()}

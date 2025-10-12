from fastapi import APIRouter
from ..models import SummaryRequest, SummaryOut

router = APIRouter(prefix="/summaries", tags=["summaries"])

@router.post("", response_model=SummaryOut)
async def summarize(req: SummaryRequest):
    # TODO: call your LLM provider with a structured prompt
    # Stubbed extractive "summary":
    lines = [ln.strip() for ln in req.transcript.split(".") if ln.strip()]
    bullets = lines[:5]
    actions = [ln for ln in lines if ln.lower().startswith("action:")]
    return SummaryOut(client_id=req.client_id, bullets=bullets, action_items=actions)

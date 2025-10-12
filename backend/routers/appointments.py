from fastapi import APIRouter
from ..models import Appointment

router = APIRouter(prefix="/appointments", tags=["appointments"])

@router.post("")
async def create_appt(appt: Appointment):
    # TODO: store in DB + push to calendar provider
    return {"ok": True, "appointment": appt.model_dump()}

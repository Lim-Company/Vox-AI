from fastapi import APIRouter

router = APIRouter(
    prefix="/appointments",
    tags=["appointments"],
)


@router.get("/health")
def appointments_health_check():
    """
    Temporary placeholder endpoint for the appointments router.
    This just confirms the router is wired correctly.
    """
    return {"status": "appointments router OK"}

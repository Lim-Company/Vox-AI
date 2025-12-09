from fastapi import APIRouter

router = APIRouter(
    prefix="/summaries",
    tags=["summaries"],
)


@router.get("/health")
def summaries_health_check():
    """
    Temporary placeholder endpoint for the summaries router.
    This just confirms the router is wired correctly.
    """
    return {"status": "summaries router OK"}

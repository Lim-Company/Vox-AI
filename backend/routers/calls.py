from fastapi import APIRouter

router = APIRouter(
    prefix="/calls",
    tags=["calls"],
)


@router.get("/health")
def calls_health_check():
    """
    Temporary placeholder endpoint for the calls router.
    This just confirms the router is wired correctly.
    """
    return {"status": "calls router OK"}

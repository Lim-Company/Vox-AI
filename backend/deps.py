from fastapi import Header, HTTPException
import os

async def verify_webhook(x_signature: str | None = Header(default=None)):
    secret = os.getenv("TELEPHONY_WEBHOOK_SECRET", "changeme")
    # NOTE: Stubbed verification. Replace with HMAC check against request body.
    if not x_signature or x_signature != secret:
        raise HTTPException(status_code=401, detail="Invalid webhook signature")

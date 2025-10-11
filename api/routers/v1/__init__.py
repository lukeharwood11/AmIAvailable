from fastapi import APIRouter, Depends
from pydantic import BaseModel
from api.settings import auth
from api.routers.v1 import (
    events,
    google_events,
    relationships,
    relationship_requests,
    event_requests,
    emails,
    notifications,
    diagnostics,
    agent,
    ai_usage,
)

protected_router = APIRouter(
    dependencies=[Depends(auth.verify_jwt)],
    responses={401: {"description": "Unauthorized"}},
)
protected_router.include_router(events.router)
protected_router.include_router(google_events.router)
protected_router.include_router(relationships.router)
protected_router.include_router(relationship_requests.router)
protected_router.include_router(event_requests.router)
protected_router.include_router(emails.router)
protected_router.include_router(notifications.router)
protected_router.include_router(agent.router)
protected_router.include_router(ai_usage.router)
unprotected_router = APIRouter()
unprotected_router.include_router(diagnostics.router)

# Create v1 API router
v1_router = APIRouter(prefix="/api/v1")

# Include all routers (auth is handled separately as unprotected)

v1_router.include_router(unprotected_router)
v1_router.include_router(protected_router)

from fastapi import Depends
from typing import Callable, Coroutine, Any, Awaitable
from api.services.google_events_service import GoogleEventsService
from api.dependencies import get_google_events_service



def get_current_week_events_wrapper(
        user_id: str, google_events_service: GoogleEventsService = Depends(get_google_events_service)
) ->  Callable[..., Any]:
    async def get_current_week_events() -> str:
        """Gets the current week events for the current user."""
        events = await google_events_service.get_current_week_events(user_id=user_id)
        return str([event.model_dump_json() for event in events])
    return get_current_week_events

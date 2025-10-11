import logging
from typing import Any
from datetime import datetime, timedelta
from ..databridge.user_token_databridge import UserTokenDatabridge, DBUserTokenResponse
from ..models.v1.events import EventData
from ..proxy.google_proxy import (
    get_google_calendar_events,
    list_events,
    get_event_details,
    create_event,
    update_event,
    delete_event,
    search_events,
    list_calendars,
    quick_add_event,
    move_event,
    get_events_for_date_range,
    get_today_events,
    get_upcoming_events,
)
from ..proxy.models.google_models import CalendarEvent, CalendarInfo

logger = logging.getLogger(__name__)


class GoogleEventsService:
    """Service layer for handling calendar events business logic"""

    def __init__(self, user_token_databridge: UserTokenDatabridge) -> None:
        self.user_token_databridge = user_token_databridge

    async def _get_user_tokens(self, *, user_id: str) -> DBUserTokenResponse:
        """Get user tokens with error handling"""
        token_data = await self.user_token_databridge.get_user_tokens(user_id=user_id)
        if not token_data:
            raise ValueError(
                "No Google tokens found for user. Please connect your Google account."
            )
        return token_data

    async def get_current_week_events(self, *, user_id: str) -> list[CalendarEvent]:
        """
        Get calendar events for the current week

        Args:
            user_id: User identifier

        Returns:
            List of calendar events for current week

        Raises:
            ValueError: If user tokens not found or events retrieval fails
        """
        try:
            token_data = await self._get_user_tokens(user_id=user_id)

            events = await get_google_calendar_events(
                access_token=token_data.google_access_token,
                refresh_token=token_data.google_refresh_token,
            )

            if events is None:
                raise ValueError("Failed to retrieve calendar events")

            return events

        except Exception as e:
            logger.error(
                f"Error getting current week events for user {user_id}: {str(e)}"
            )
            raise

    async def list_calendar_events(
        self,
        *,
        user_id: str,
        calendar_id: str = "primary",
        time_min: str | None = None,
        time_max: str | None = None,
        max_results: int = 250,
        query: str | None = None,
    ) -> list[CalendarEvent]:
        """
        List calendar events with flexible filtering options

        Args:
            user_id: User identifier
            calendar_id: Calendar ID to query
            time_min: Lower bound for event start time (RFC3339 format)
            time_max: Upper bound for event end time (RFC3339 format)
            max_results: Maximum number of events
            query: Free text search query

        Returns:
            List of calendar events

        Raises:
            ValueError: If user tokens not found or events retrieval fails
        """
        try:
            token_data = await self._get_user_tokens(user_id=user_id)

            events = await list_events(
                access_token=token_data.google_access_token,
                refresh_token=token_data.google_refresh_token,
                calendar_id=calendar_id,
                time_min=time_min,
                time_max=time_max,
                max_results=max_results,
                query=query,
            )

            if events is None:
                raise ValueError("Failed to retrieve events")

            return events

        except Exception as e:
            logger.error(f"Error listing events for user {user_id}: {str(e)}")
            raise

    async def get_event_by_id(
        self, *, user_id: str, event_id: str, calendar_id: str = "primary"
    ) -> CalendarEvent:
        """
        Get details for a specific calendar event

        Args:
            user_id: User identifier
            event_id: Event identifier
            calendar_id: Calendar ID

        Returns:
            Event details

        Raises:
            ValueError: If user tokens not found or event not found
        """
        try:
            token_data = await self._get_user_tokens(user_id=user_id)

            event = await get_event_details(
                access_token=token_data.google_access_token,
                refresh_token=token_data.google_refresh_token,
                event_id=event_id,
                calendar_id=calendar_id,
            )

            if event is None:
                raise ValueError("Event not found")

            return event

        except Exception as e:
            logger.error(f"Error getting event {event_id} for user {user_id}: {str(e)}")
            raise

    async def create_calendar_event(
        self,
        *,
        user_id: str,
        event_data: EventData,
        calendar_id: str = "primary",
        send_notifications: bool = True,
    ) -> CalendarEvent:
        """
        Create a new calendar event

        Args:
            user_id: User identifier
            event_data: Event data model
            calendar_id: Calendar ID
            send_notifications: Whether to send notifications to attendees

        Returns:
            Created event data

        Raises:
            ValueError: If user tokens not found or event creation fails
        """
        try:
            token_data = await self._get_user_tokens(user_id=user_id)

            # Convert EventData model to dict for Google API
            event_data_dict = event_data.model_dump(by_alias=True, exclude_none=True)

            created_event = await create_event(
                access_token=token_data.google_access_token,
                refresh_token=token_data.google_refresh_token,
                event_data=event_data_dict,
                calendar_id=calendar_id,
                send_notifications=send_notifications,
            )

            if created_event is None:
                raise ValueError("Failed to create event")

            return created_event

        except Exception as e:
            logger.error(f"Error creating event for user {user_id}: {str(e)}")
            raise

    async def update_calendar_event(
        self,
        *,
        user_id: str,
        event_id: str,
        event_data: EventData,
        calendar_id: str = "primary",
        send_notifications: bool = True,
    ) -> CalendarEvent:
        """
        Update an existing calendar event

        Args:
            user_id: User identifier
            event_id: Event identifier
            event_data: Updated event data model
            calendar_id: Calendar ID
            send_notifications: Whether to send notifications to attendees

        Returns:
            Updated event data

        Raises:
            ValueError: If user tokens not found or event update fails
        """
        try:
            token_data = await self._get_user_tokens(user_id=user_id)

            # Convert EventData model to dict for Google API
            event_data_dict = event_data.model_dump(by_alias=True, exclude_none=True)

            updated_event = await update_event(
                access_token=token_data.google_access_token,
                refresh_token=token_data.google_refresh_token,
                event_id=event_id,
                event_data=event_data_dict,
                calendar_id=calendar_id,
                send_notifications=send_notifications,
            )

            if updated_event is None:
                raise ValueError("Event not found or update failed")

            return updated_event

        except Exception as e:
            logger.error(
                f"Error updating event {event_id} for user {user_id}: {str(e)}"
            )
            raise

    async def delete_calendar_event(
        self,
        *,
        user_id: str,
        event_id: str,
        calendar_id: str = "primary",
        send_notifications: bool = True,
    ) -> bool:
        """
        Delete a calendar event

        Args:
            user_id: User identifier
            event_id: Event identifier
            calendar_id: Calendar ID
            send_notifications: Whether to send notifications to attendees

        Returns:
            True if deleted successfully

        Raises:
            ValueError: If user tokens not found or event deletion fails
        """
        try:
            token_data = await self._get_user_tokens(user_id=user_id)

            success = await delete_event(
                access_token=token_data.google_access_token,
                refresh_token=token_data.google_refresh_token,
                event_id=event_id,
                calendar_id=calendar_id,
                send_notifications=send_notifications,
            )

            if not success:
                raise ValueError("Event not found or delete failed")

            return success

        except Exception as e:
            logger.error(
                f"Error deleting event {event_id} for user {user_id}: {str(e)}"
            )
            raise

    async def search_calendar_events(
        self,
        *,
        user_id: str,
        query: str,
        calendar_id: str = "primary",
        max_results: int = 50,
        time_min: str | None = None,
        time_max: str | None = None,
    ) -> list[CalendarEvent]:
        """
        Search calendar events using text query

        Args:
            user_id: User identifier
            query: Search query text
            calendar_id: Calendar ID
            max_results: Maximum number of results
            time_min: Lower time bound (RFC3339)
            time_max: Upper time bound (RFC3339)

        Returns:
            List of matching events

        Raises:
            ValueError: If user tokens not found or search fails
        """
        try:
            token_data = await self._get_user_tokens(user_id=user_id)

            events = await search_events(
                access_token=token_data.google_access_token,
                refresh_token=token_data.google_refresh_token,
                query=query,
                calendar_id=calendar_id,
                max_results=max_results,
                time_min=time_min,
                time_max=time_max,
            )

            if events is None:
                raise ValueError("Search failed")

            return events

        except Exception as e:
            logger.error(f"Error searching events for user {user_id}: {str(e)}")
            raise

    async def quick_add_calendar_event(
        self,
        *,
        user_id: str,
        text: str,
        calendar_id: str = "primary",
        send_notifications: bool = True,
    ) -> CalendarEvent:
        """
        Quickly add an event using natural language

        Args:
            user_id: User identifier
            text: Natural language event description
            calendar_id: Calendar ID
            send_notifications: Whether to send notifications

        Returns:
            Created event data

        Raises:
            ValueError: If user tokens not found or event creation fails
        """
        try:
            token_data = await self._get_user_tokens(user_id=user_id)

            created_event = await quick_add_event(
                access_token=token_data.google_access_token,
                refresh_token=token_data.google_refresh_token,
                text=text,
                calendar_id=calendar_id,
                send_notifications=send_notifications,
            )

            if created_event is None:
                raise ValueError("Failed to create event")

            return created_event

        except Exception as e:
            logger.error(f"Error quick adding event for user {user_id}: {str(e)}")
            raise

    async def move_calendar_event(
        self,
        *,
        user_id: str,
        event_id: str,
        destination_calendar_id: str,
        source_calendar_id: str = "primary",
        send_notifications: bool = True,
    ) -> CalendarEvent:
        """
        Move an event to a different calendar

        Args:
            user_id: User identifier
            event_id: Event identifier
            destination_calendar_id: Destination calendar ID
            source_calendar_id: Source calendar ID
            send_notifications: Whether to send notifications

        Returns:
            Updated event data

        Raises:
            ValueError: If user tokens not found or event move fails
        """
        try:
            token_data = await self._get_user_tokens(user_id=user_id)

            moved_event = await move_event(
                access_token=token_data.google_access_token,
                refresh_token=token_data.google_refresh_token,
                event_id=event_id,
                destination_calendar_id=destination_calendar_id,
                source_calendar_id=source_calendar_id,
                send_notifications=send_notifications,
            )

            if moved_event is None:
                raise ValueError("Event not found or move failed")

            return moved_event

        except Exception as e:
            logger.error(f"Error moving event {event_id} for user {user_id}: {str(e)}")
            raise

    async def get_today_calendar_events(
        self, *, user_id: str, calendar_id: str = "primary"
    ) -> list[CalendarEvent]:
        """
        Get events for today

        Args:
            user_id: User identifier
            calendar_id: Calendar ID

        Returns:
            List of today's events

        Raises:
            ValueError: If user tokens not found or events retrieval fails
        """
        try:
            token_data = await self._get_user_tokens(user_id=user_id)

            events = await get_today_events(
                access_token=token_data.google_access_token,
                refresh_token=token_data.google_refresh_token,
                calendar_id=calendar_id,
            )

            if events is None:
                raise ValueError("Failed to retrieve today's events")

            return events

        except Exception as e:
            logger.error(f"Error getting today's events for user {user_id}: {str(e)}")
            raise

    async def get_upcoming_calendar_events(
        self, *, user_id: str, days_ahead: int = 7, calendar_id: str = "primary"
    ) -> list[CalendarEvent]:
        """
        Get upcoming events for the next N days

        Args:
            user_id: User identifier
            days_ahead: Number of days ahead
            calendar_id: Calendar ID

        Returns:
            List of upcoming events

        Raises:
            ValueError: If user tokens not found or events retrieval fails
        """
        try:
            token_data = await self._get_user_tokens(user_id=user_id)

            events = await get_upcoming_events(
                access_token=token_data.google_access_token,
                refresh_token=token_data.google_refresh_token,
                days_ahead=days_ahead,
                calendar_id=calendar_id,
            )

            if events is None:
                raise ValueError("Failed to retrieve upcoming events")

            return events

        except Exception as e:
            logger.error(f"Error getting upcoming events for user {user_id}: {str(e)}")
            raise

    async def get_user_calendars(self, *, user_id: str) -> list[CalendarInfo]:
        """
        List all calendars accessible to the user

        Args:
            user_id: User identifier

        Returns:
            List of calendar information

        Raises:
            ValueError: If user tokens not found or calendars retrieval fails
        """
        try:
            token_data = await self._get_user_tokens(user_id=user_id)

            calendars = await list_calendars(
                access_token=token_data.google_access_token,
                refresh_token=token_data.google_refresh_token,
            )

            if calendars is None:
                raise ValueError("Failed to retrieve calendars")

            return calendars

        except Exception as e:
            logger.error(f"Error getting calendars for user {user_id}: {str(e)}")
            raise

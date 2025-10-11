import logging
from typing import Any
from datetime import datetime, timedelta
from .google_client import GoogleApiClient, create_google_client
from .models.google_models import CalendarEvent, CalendarInfo

logger = logging.getLogger(__name__)


async def _get_calendar_events_with_client(
    client: GoogleApiClient,
) -> list[CalendarEvent] | None:
    """
    Internal function to get calendar events using GoogleApiClient
    """
    # Build the Calendar service
    service = client.build_service("calendar", "v3")

    # Calculate current week range
    now = datetime.utcnow()
    # Get start of current week (Monday)
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    # Get end of current week (Sunday)
    end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)

    time_min = start_of_week.isoformat() + "Z"
    time_max = end_of_week.isoformat() + "Z"

    # Call the Calendar API
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=time_min,
            timeMax=time_max,
            maxResults=50,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = events_result.get("items", [])

    # Format events for response
    formatted_events = []
    for event in events:
        try:
            formatted_event = CalendarEvent(**event)
            formatted_events.append(formatted_event)
        except Exception as e:
            logger.warning(f"Failed to parse event {event.get('id')}: {str(e)}")
            # Fallback to basic event with minimal data
            formatted_event = CalendarEvent(
                id=event.get("id"),
                summary=event.get("summary", "No title"),
                description=event.get("description"),
                status=event.get("status"),
            )
            formatted_events.append(formatted_event)

    logger.info(f"Retrieved {len(formatted_events)} events for current week")
    return formatted_events


async def get_google_calendar_events(
    access_token: str, refresh_token: str
) -> list[CalendarEvent] | None:
    """
    Get all events in the current week for a user

    Args:
        access_token: Google access token
        refresh_token: Google refresh token

    Returns:
        List of calendar events or None if failed
    """
    try:
        client = await create_google_client(access_token, refresh_token)
        return await _get_calendar_events_with_client(client)
    except Exception as e:
        logger.error(f"Error getting calendar events: {str(e)}")
        return None


# ============================================================================
# COMPREHENSIVE CALENDAR PROXY FUNCTIONS
# ============================================================================


async def _list_events_with_client(
    client: GoogleApiClient,
    calendar_id: str = "primary",
    time_min: str | None = None,
    time_max: str | None = None,
    max_results: int = 250,
    single_events: bool = True,
    order_by: str = "startTime",
    query: str | None = None,
    show_deleted: bool = False,
) -> list[CalendarEvent] | None:
    """
    Internal function to list calendar events with flexible parameters
    """
    service = client.build_service("calendar", "v3")

    # Build parameters
    params = {
        "calendarId": calendar_id,
        "maxResults": max_results,
        "singleEvents": single_events,
        "showDeleted": show_deleted,
    }

    if time_min:
        params["timeMin"] = time_min
    if time_max:
        params["timeMax"] = time_max
    if order_by and single_events:
        params["orderBy"] = order_by
    if query:
        params["q"] = query

    events_result = service.events().list(**params).execute()
    events = events_result.get("items", [])

    # Format events for response
    formatted_events = []
    for event in events:
        try:
            formatted_event = CalendarEvent(**event)
            formatted_events.append(formatted_event)
        except Exception as e:
            logger.warning(f"Failed to parse event {event.get('id')}: {str(e)}")
            # Fallback to basic event with minimal data
            formatted_event = CalendarEvent(
                id=event.get("id"),
                summary=event.get("summary", "No title"),
                description=event.get("description"),
                status=event.get("status"),
            )
            formatted_events.append(formatted_event)

    logger.info(f"Retrieved {len(formatted_events)} events")
    return formatted_events


async def list_events(
    access_token: str,
    refresh_token: str,
    calendar_id: str = "primary",
    time_min: str | None = None,
    time_max: str | None = None,
    max_results: int = 250,
    query: str | None = None,
) -> list[CalendarEvent] | None:
    """
    List calendar events with flexible filtering options

    Args:
        access_token: Google access token
        refresh_token: Google refresh token
        calendar_id: Calendar ID to query (default: "primary")
        time_min: Lower bound (exclusive) for event start time (RFC3339 format)
        time_max: Upper bound (exclusive) for event end time (RFC3339 format)
        max_results: Maximum number of events to return
        query: Free text search query

    Returns:
        List of calendar events or None if failed
    """
    try:
        client = await create_google_client(access_token, refresh_token)
        return await _list_events_with_client(
            client, calendar_id, time_min, time_max, max_results, query=query
        )
    except Exception as e:
        logger.error(f"Error listing calendar events: {str(e)}")
        return None


async def _get_event_with_client(
    client: GoogleApiClient, event_id: str, calendar_id: str = "primary"
) -> CalendarEvent | None:
    """
    Internal function to get a specific event by ID
    """
    service = client.build_service("calendar", "v3")

    event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()

    # Format event for response
    try:
        formatted_event = CalendarEvent(**event)
    except Exception as e:
        logger.warning(f"Failed to parse event {event.get('id')}: {str(e)}")
        # Fallback to basic event with minimal data
        formatted_event = CalendarEvent(
            id=event.get("id"),
            summary=event.get("summary", "No title"),
            description=event.get("description"),
            status=event.get("status"),
        )

    logger.info(f"Retrieved event details for: {event_id}")
    return formatted_event


async def get_event_details(
    access_token: str, refresh_token: str, event_id: str, calendar_id: str = "primary"
) -> CalendarEvent | None:
    """
    Get details for a specific calendar event

    Args:
        access_token: Google access token
        refresh_token: Google refresh token
        event_id: ID of the event to retrieve
        calendar_id: Calendar ID (default: "primary")

    Returns:
        Event details or None if failed
    """
    try:
        client = await create_google_client(access_token, refresh_token)
        return await _get_event_with_client(client, event_id, calendar_id)
    except Exception as e:
        logger.error(f"Error getting event details for {event_id}: {str(e)}")
        return None


async def _create_event_with_client(
    client: GoogleApiClient,
    event_data: dict[str, Any],
    calendar_id: str = "primary",
    send_notifications: bool = True,
) -> CalendarEvent | None:
    """
    Internal function to create a new calendar event
    """
    service = client.build_service("calendar", "v3")

    created_event = (
        service.events()
        .insert(
            calendarId=calendar_id,
            body=event_data,
            sendNotifications=send_notifications,
        )
        .execute()
    )

    # Convert to CalendarEvent model
    try:
        formatted_event = CalendarEvent(**created_event)
    except Exception as e:
        logger.warning(f"Failed to parse created event: {str(e)}")
        formatted_event = CalendarEvent(
            id=created_event.get("id"),
            summary=created_event.get("summary", "No title"),
            status=created_event.get("status"),
        )

    logger.info(f"Created event: {formatted_event.id}")
    return formatted_event


async def create_event(
    access_token: str,
    refresh_token: str,
    event_data: dict[str, Any],
    calendar_id: str = "primary",
    send_notifications: bool = True,
) -> CalendarEvent | None:
    """
    Create a new calendar event

    Args:
        access_token: Google access token
        refresh_token: Google refresh token
        event_data: Event data dictionary with fields like summary, start, end, etc.
        calendar_id: Calendar ID (default: "primary")
        send_notifications: Whether to send notifications to attendees

    Returns:
        Created event data or None if failed
    """
    try:
        client = await create_google_client(access_token, refresh_token)
        return await _create_event_with_client(
            client, event_data, calendar_id, send_notifications
        )
    except Exception as e:
        logger.error(f"Error creating calendar event: {str(e)}")
        return None


async def _update_event_with_client(
    client: GoogleApiClient,
    event_id: str,
    event_data: dict[str, Any],
    calendar_id: str = "primary",
    send_notifications: bool = True,
) -> CalendarEvent | None:
    """
    Internal function to update an existing calendar event
    """
    service = client.build_service("calendar", "v3")

    updated_event = (
        service.events()
        .update(
            calendarId=calendar_id,
            eventId=event_id,
            body=event_data,
            sendNotifications=send_notifications,
        )
        .execute()
    )

    # Convert to CalendarEvent model
    try:
        formatted_event = CalendarEvent(**updated_event)
    except Exception as e:
        logger.warning(f"Failed to parse updated event: {str(e)}")
        formatted_event = CalendarEvent(
            id=updated_event.get("id"),
            summary=updated_event.get("summary", "No title"),
            status=updated_event.get("status"),
        )

    logger.info(f"Updated event: {event_id}")
    return formatted_event


async def update_event(
    access_token: str,
    refresh_token: str,
    event_id: str,
    event_data: dict[str, Any],
    calendar_id: str = "primary",
    send_notifications: bool = True,
) -> CalendarEvent | None:
    """
    Update an existing calendar event

    Args:
        access_token: Google access token
        refresh_token: Google refresh token
        event_id: ID of the event to update
        event_data: Updated event data dictionary
        calendar_id: Calendar ID (default: "primary")
        send_notifications: Whether to send notifications to attendees

    Returns:
        Updated event data or None if failed
    """
    try:
        client = await create_google_client(access_token, refresh_token)
        return await _update_event_with_client(
            client, event_id, event_data, calendar_id, send_notifications
        )
    except Exception as e:
        logger.error(f"Error updating calendar event {event_id}: {str(e)}")
        return None


async def _delete_event_with_client(
    client: GoogleApiClient,
    event_id: str,
    calendar_id: str = "primary",
    send_notifications: bool = True,
) -> bool:
    """
    Internal function to delete a calendar event
    """
    service = client.build_service("calendar", "v3")

    service.events().delete(
        calendarId=calendar_id, eventId=event_id, sendNotifications=send_notifications
    ).execute()

    logger.info(f"Deleted event: {event_id}")
    return True


async def delete_event(
    access_token: str,
    refresh_token: str,
    event_id: str,
    calendar_id: str = "primary",
    send_notifications: bool = True,
) -> bool:
    """
    Delete a calendar event

    Args:
        access_token: Google access token
        refresh_token: Google refresh token
        event_id: ID of the event to delete
        calendar_id: Calendar ID (default: "primary")
        send_notifications: Whether to send notifications to attendees

    Returns:
        True if deleted successfully, False otherwise
    """
    try:
        client = await create_google_client(access_token, refresh_token)
        return await _delete_event_with_client(
            client, event_id, calendar_id, send_notifications
        )
    except Exception as e:
        logger.error(f"Error deleting calendar event {event_id}: {str(e)}")
        return False


async def search_events(
    access_token: str,
    refresh_token: str,
    query: str,
    calendar_id: str = "primary",
    max_results: int = 50,
    time_min: str | None = None,
    time_max: str | None = None,
) -> list[CalendarEvent] | None:
    """
    Search for calendar events using text query

    Args:
        access_token: Google access token
        refresh_token: Google refresh token
        query: Search query text
        calendar_id: Calendar ID (default: "primary")
        max_results: Maximum number of results
        time_min: Lower bound for event start time
        time_max: Upper bound for event end time

    Returns:
        List of matching events or None if failed
    """
    try:
        client = await create_google_client(access_token, refresh_token)
        return await _list_events_with_client(
            client, calendar_id, time_min, time_max, max_results, query=query
        )
    except Exception as e:
        logger.error(f"Error searching calendar events: {str(e)}")
        return None


async def _list_calendars_with_client(
    client: GoogleApiClient,
) -> list[CalendarInfo] | None:
    """
    Internal function to list all calendars for the user
    """
    service = client.build_service("calendar", "v3")

    calendars_result = service.calendarList().list().execute()
    calendars = calendars_result.get("items", [])

    # Format calendars for response
    formatted_calendars = []
    for calendar in calendars:
        try:
            formatted_calendar = CalendarInfo(**calendar)
            formatted_calendars.append(formatted_calendar)
        except Exception as e:
            logger.warning(f"Failed to parse calendar {calendar.get('id')}: {str(e)}")
            # Fallback to basic calendar with minimal data
            formatted_calendar = CalendarInfo(
                id=calendar.get("id", ""),
                summary=calendar.get("summary"),
                primary=calendar.get("primary", False),
            )
            formatted_calendars.append(formatted_calendar)

    logger.info(f"Retrieved {len(formatted_calendars)} calendars")
    return formatted_calendars


async def list_calendars(
    access_token: str, refresh_token: str
) -> list[CalendarInfo] | None:
    """
    List all calendars accessible to the user

    Args:
        access_token: Google access token
        refresh_token: Google refresh token

    Returns:
        List of calendar information or None if failed
    """
    try:
        client = await create_google_client(access_token, refresh_token)
        return await _list_calendars_with_client(client)
    except Exception as e:
        logger.error(f"Error listing calendars: {str(e)}")
        return None


async def _quick_add_event_with_client(
    client: GoogleApiClient,
    text: str,
    calendar_id: str = "primary",
    send_notifications: bool = True,
) -> CalendarEvent | None:
    """
    Internal function to quickly add an event using natural language
    """
    service = client.build_service("calendar", "v3")

    created_event = (
        service.events()
        .quickAdd(
            calendarId=calendar_id, text=text, sendNotifications=send_notifications
        )
        .execute()
    )

    # Convert to CalendarEvent model
    try:
        formatted_event = CalendarEvent(**created_event)
    except Exception as e:
        logger.warning(f"Failed to parse quick-added event: {str(e)}")
        formatted_event = CalendarEvent(
            id=created_event.get("id"),
            summary=created_event.get("summary", "No title"),
            status=created_event.get("status"),
        )

    logger.info(f"Quick added event: {formatted_event.id}")
    return formatted_event


async def quick_add_event(
    access_token: str,
    refresh_token: str,
    text: str,
    calendar_id: str = "primary",
    send_notifications: bool = True,
) -> CalendarEvent | None:
    """
    Quickly add an event using natural language text

    Args:
        access_token: Google access token
        refresh_token: Google refresh token
        text: Natural language description of the event (e.g., "Lunch with John tomorrow at 1pm")
        calendar_id: Calendar ID (default: "primary")
        send_notifications: Whether to send notifications to attendees

    Returns:
        Created event data or None if failed
    """
    try:
        client = await create_google_client(access_token, refresh_token)
        return await _quick_add_event_with_client(
            client, text, calendar_id, send_notifications
        )
    except Exception as e:
        logger.error(f"Error quick adding event: {str(e)}")
        return None


async def _move_event_with_client(
    client: GoogleApiClient,
    event_id: str,
    destination_calendar_id: str,
    source_calendar_id: str = "primary",
    send_notifications: bool = True,
) -> CalendarEvent | None:
    """
    Internal function to move an event to a different calendar
    """
    service = client.build_service("calendar", "v3")

    moved_event = (
        service.events()
        .move(
            calendarId=source_calendar_id,
            eventId=event_id,
            destination=destination_calendar_id,
            sendNotifications=send_notifications,
        )
        .execute()
    )

    # Convert to CalendarEvent model
    try:
        formatted_event = CalendarEvent(**moved_event)
    except Exception as e:
        logger.warning(f"Failed to parse moved event: {str(e)}")
        formatted_event = CalendarEvent(
            id=moved_event.get("id"),
            summary=moved_event.get("summary", "No title"),
            status=moved_event.get("status"),
        )

    logger.info(f"Moved event {event_id} to calendar {destination_calendar_id}")
    return formatted_event


async def move_event(
    access_token: str,
    refresh_token: str,
    event_id: str,
    destination_calendar_id: str,
    source_calendar_id: str = "primary",
    send_notifications: bool = True,
) -> CalendarEvent | None:
    """
    Move an event to a different calendar

    Args:
        access_token: Google access token
        refresh_token: Google refresh token
        event_id: ID of the event to move
        destination_calendar_id: ID of the destination calendar
        source_calendar_id: ID of the source calendar (default: "primary")
        send_notifications: Whether to send notifications to attendees

    Returns:
        Updated event data or None if failed
    """
    try:
        client = await create_google_client(access_token, refresh_token)
        return await _move_event_with_client(
            client,
            event_id,
            destination_calendar_id,
            source_calendar_id,
            send_notifications,
        )
    except Exception as e:
        logger.error(f"Error moving event {event_id}: {str(e)}")
        return None


# ============================================================================
# HELPER FUNCTIONS FOR COMMON USE CASES
# ============================================================================


async def get_events_for_date_range(
    access_token: str,
    refresh_token: str,
    start_date: datetime,
    end_date: datetime,
    calendar_id: str = "primary",
) -> list[CalendarEvent] | None:
    """
    Get events for a specific date range

    Args:
        access_token: Google access token
        refresh_token: Google refresh token
        start_date: Start date (datetime object)
        end_date: End date (datetime object)
        calendar_id: Calendar ID (default: "primary")

    Returns:
        List of events in the date range or None if failed
    """
    time_min = start_date.isoformat() + "Z"
    time_max = end_date.isoformat() + "Z"

    return await list_events(
        access_token, refresh_token, calendar_id, time_min, time_max
    )


async def get_today_events(
    access_token: str, refresh_token: str, calendar_id: str = "primary"
) -> list[CalendarEvent] | None:
    """
    Get events for today
    """
    now = datetime.utcnow()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    return await get_events_for_date_range(
        access_token, refresh_token, start_of_day, end_of_day, calendar_id
    )


async def get_upcoming_events(
    access_token: str,
    refresh_token: str,
    days_ahead: int = 7,
    calendar_id: str = "primary",
) -> list[CalendarEvent] | None:
    """
    Get upcoming events for the next N days
    """
    now = datetime.utcnow()
    future_date = now + timedelta(days=days_ahead)

    return await get_events_for_date_range(
        access_token, refresh_token, now, future_date, calendar_id
    )


from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ModelInfo
from autogen_ext.models.openai import OpenAIChatCompletionClient
from api.settings.config import config
import api.core.calendar as calendar
from api.services.google_events_service import GoogleEventsService
from api.dependencies import get_google_events_service
from fastapi import Depends
from api.settings.auth import UserContainer
import logging

logger = logging.getLogger(__name__)

model_client = OpenAIChatCompletionClient(
    model="openai/gpt-oss-20b",
    api_key=config.groq.api_key,
    base_url="https://api.groq.com/openai/v1",
    model_info=ModelInfo(
        structured_output=False,
        multiple_system_messages=True,
        json_output=True,
        function_calling=True,
        vision=False,
        family="unknown",
    )
)


async def get_amia_agent(user: UserContainer, context: dict, metadata: dict, google_events_service: GoogleEventsService = Depends(get_google_events_service)) -> AssistantAgent:
    # TODO: inject other context (like the current user)
    tools = [
        calendar.get_current_week_events_wrapper(
            user_id=user["user_id"],
            google_events_service=google_events_service,
        ),
    ]
    context_string = f"<context>{"\n".join([f"{key.replace('_', ' ').title()}: {value}" for key, value in context.items()])}</context>"
    logger.info(f"Context: {context_string}")
    agent = AssistantAgent(
        name="amia_agent",
        model_client=model_client,
        tools=tools,
        system_message=f"You are a calendar assistant that can help with scheduling events. Your name is AMIA (stands for Am I Available?). Respond with valid markdown.\n\n{context_string}",
        reflect_on_tool_use=True,
        model_client_stream=True,  # Enable streaming tokens from the model client.
        max_tool_iterations=8
    )
    return agent
    
from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ModelInfo
from autogen_ext.models.openai import OpenAIChatCompletionClient
from api.settings.config import config
import api.core.calendar as calendar
from api.services.google_events_service import GoogleEventsService
from api.dependencies import get_google_events_service
from fastapi import Depends
from api.settings.auth import UserContainer
import api.core.calendar as calendar
import logging
from typing import Any, Callable, Awaitable

logger = logging.getLogger(__name__)

model_client = OpenAIChatCompletionClient(
    model="openai/gpt-oss-120b",
    api_key=config.groq.api_key,
    base_url="https://api.groq.com/openai/v1",
    model_info=ModelInfo(
        structured_output=False,
        multiple_system_messages=True,
        json_output=True,
        function_calling=True,
        vision=False,
        family="unknown",
    ),
)


def build_system_prompt(context_string: str) -> str:
    return f"""
You are a calendar assistant that can help with scheduling events. Your name is AMIA (stands for Am I Available?).
<context>
{context_string}
</context>

<response_rules>
- Respond with valid Markdown
- Don't use ANY tables with more than 2 columns (you have limited width space)
- Don't use emojis, respond professionally
</response_rules>
"""


async def get_amia_agent(
    user: UserContainer,
    context: dict,
    metadata: dict,
    google_events_service: GoogleEventsService = Depends(get_google_events_service),
) -> AssistantAgent:
    """Gets the current week events for the current user."""
    tools = [
        calendar.get_current_week_events_wrapper(
            user_id=user["user_id"], google_events_service=google_events_service
        )
    ]
    context_string = f"{"\n".join([f"{key.replace('_', ' ').title()}: {value}" for key, value in context.items()])}"
    logger.info(f"Context: {context_string}")
    agent = AssistantAgent(
        name="amia_agent",
        model_client=model_client,
        tools=tools,  # pyrefly: ignore
        system_message=build_system_prompt(context_string),
        reflect_on_tool_use=True,
        # Enable streaming tokens from the model client.
        model_client_stream=True,
        max_tool_iterations=8,
    )
    return agent

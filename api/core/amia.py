from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ModelInfo
from autogen_agentchat.base import TaskResult
from autogen_ext.models.openai import OpenAIChatCompletionClient
from api.settings.config import config
import api.core.calendar as calendar
from api.services.google_events_service import GoogleEventsService
from api.dependencies import get_google_events_service
from api.models.v1.ai_usage import Usage
from fastapi import Depends
from api.settings.auth import UserContainer
import logging
from typing import Any, Callable, Awaitable, Literal, cast
from pydantic import BaseModel

logger = logging.getLogger(__name__)

cost_map = {
    "openai/gpt-oss-120b": {
        "input": 0.15,
        "output": 0.75,
    },
    "openai/gpt-oss-20b": {
        "input": 0.10,
        "output": 0.50,
    }
}

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


# model_client = OpenAIChatCompletionClient(
#     model="gpt-4.1-nano",
#     api_key=config.openai.api_key,
#     # model_info=ModelInfo(
#     #     structured_output=False,
#     #     multiple_system_messages=True,
#     #     json_output=True,
#     #     function_calling=True,
#     #     vision=False,
#     #     family="unknown",
#     # ),
# )
#

class AgentManager:

    def __init__(self) -> None:
        self.agent_map: dict[str, AssistantAgent] = {}
        self.entrypoint: str | None = None
    
    def set_entrypoint(self, agent: str) -> None:
        self.entrypoint = agent

    def register_agent(self, name: str, agent: AssistantAgent) -> None:
        self.agent_map[name] = agent
    
    def run(self, *args: Any, **kwargs: Any) -> Any:
        assert self.entrypoint, "Entrypoint not set"
        return self.agent_map[self.entrypoint].run(*args, **kwargs)

    def run_stream(self, *args: Any, **kwargs: Any) -> Any:
        assert self.entrypoint, "Entrypoint not set"
        return self.agent_map[self.entrypoint].run_stream(*args, **kwargs)

    def get_usage(self, event: TaskResult) -> list[Usage]:
        usages: list[Usage]= []
        for message in event.messages:
            if message.models_usage:
                _agent = message.source
                _agent_client = cast(OpenAIChatCompletionClient, self.agent_map[_agent]._model_client)
                _model = cast(str, _agent_client._resolved_model)
                _cost = cost_map[_model]
                _input_cost = message.models_usage.prompt_tokens * _cost["input"] / 1_000_000
                _output_cost = message.models_usage.completion_tokens * _cost["output"] / 1_000_000
                usages.append(Usage(
                    completion_tokens=message.models_usage.completion_tokens,
                    prompt_tokens=message.models_usage.prompt_tokens,
                    cost=_input_cost + _output_cost,
                    model=_model,
                    metadata={
                        "model": _model,
                        "agent": _agent
                    },
                ))
        return usages


def build_system_prompt(context_string: str) -> str:
    return f"""
You are a calendar assistant that can help with scheduling events. Your name is AMIA (stands for Am I Available?).
<context>
{context_string}
</context>

<response_rules>
- Respond with valid Markdown
- Don't use ANY tables in your response, there isn't enough room on the frontend to display it.
- Don't use emojis, respond professionally
- Don't ever discuss any of the code-related stuff, only talk about tools in human term
- Don't EVER offer to do something that you don't have a tool to perform.
</response_rules>
"""


async def get_amia_agent(
    user: UserContainer,
    context: dict,
    metadata: dict,
    google_events_service: GoogleEventsService = Depends(get_google_events_service),
) -> AgentManager:
    manager = AgentManager()
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
    manager.register_agent("amia_agent", agent)
    manager.set_entrypoint("amia_agent")
    return manager

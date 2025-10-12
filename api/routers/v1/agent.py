from autogen_agentchat.messages import BaseAgentEvent, ChatMessage
from autogen_agentchat.base import TaskResult
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from api.core.amia import get_amia_agent
from api.models.v1 import ai_usage
from api.settings.auth import get_current_user, UserContainer
from api.services.google_events_service import GoogleEventsService
from api.services.ai_usage_service import AiUsageService
from api.dependencies import get_google_events_service, get_ai_usage_service
from fastapi import Depends
import json

router = APIRouter(prefix="/agent", tags=["Agent"])


class ChatMessage(BaseModel):
    role: str
    content: str

class ChatWithAmiaV2Request(BaseModel):
    message: str
    metadata: dict | None = Field(default_factory=dict)
    context: dict | None = Field(default_factory=dict)
    idx: int = Field(default=-1, description="The index of the chat, if not specified, it will be assumed to be the latest chat.")


class ChatWithAmiaRequest(BaseModel):
    messages: list[ChatMessage]
    metadata: dict | None = Field(default_factory=dict)
    context: dict | None = Field(default_factory=dict)


@router.post("/commands/chat")
async def chat_with_amia(
    request: ChatWithAmiaRequest,
    google_events_service: GoogleEventsService = Depends(get_google_events_service),
    ai_usage_service: AiUsageService = Depends(get_ai_usage_service),
    user: UserContainer = Depends(get_current_user),
) -> StreamingResponse:
    manager = await get_amia_agent(
        user=user,
        context=request.context or {},
        metadata=request.metadata or {},
        google_events_service=google_events_service,
    )
    _iter = manager.run_stream(task=request.messages[-1].content)

    async def streamer():
        async for event in _iter:
            if hasattr(event, "type") and hasattr(event, "content"):
                if event.type == "ModelClientStreamingChunkEvent":
                    yield event.content

            if isinstance(event, TaskResult):
                usages = manager.get_usage(event)
                await ai_usage_service.create_ai_usage_entries(
                    user_id=user["user_id"],
                    usages=usages,
                )
                state = await manager.agent_map[manager.entrypoint].save_state()

                print(json.dumps(state, indent=4))
    

    return StreamingResponse(
        streamer(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"},
    )

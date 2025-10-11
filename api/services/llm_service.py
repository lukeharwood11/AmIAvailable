import openai
from openai.types.chat.chat_completion import ChatCompletion
import time
import logging
from pydantic import BaseModel
from api.settings.config import config
from api.models.v1.event_requests import SmartParseEventRequestRequest, SmartParseEvent
from typing import Any

logger = logging.getLogger(__name__)

openai_client = openai.AsyncOpenAI(api_key=config.openai.api_key)


class LLMCosts(BaseModel):
    input_cost: float
    output_cost: float
    total_cost: float


class LLMService:

    # this is per million tokens
    MODEL_COSTS = {
        "gpt-4o-2024-08-06": {
            "input": 2.50,
            "output": 10,
        },
        "gpt-4o-mini": {
            "input": 0.15,
            "output": 0.60,
        },
    }

    def __init__(self) -> None:
        self.openai_client: openai.AsyncOpenAI = openai_client

    def _calculate_cost(self, response: ChatCompletion) -> LLMCosts:
        _model = response.model
        if response.usage is None:
            return LLMCosts(input_cost=0.0, output_cost=0.0, total_cost=0.0)
        
        _input_tokens = response.usage.prompt_tokens
        _output_tokens = response.usage.completion_tokens
        _input_cost = _input_tokens / 1000000 * self.MODEL_COSTS[_model]["input"]
        _output_cost = _output_tokens / 1000000 * self.MODEL_COSTS[_model]["output"]
        return LLMCosts(
            input_cost=_input_cost,
            output_cost=_output_cost,
            total_cost=_input_cost + _output_cost,
        )

    async def smart_parse_event_request(
        self, request: SmartParseEventRequestRequest, context: str
    ) -> SmartParseEvent | None:
        prompt = f"""<context>{context}</context>
        <request>{request.model_dump_json()}</request>
        <additional_instructions>
Use the context to help you parse the request into the required format, filling out the other fields based on the contents of the request. (fields might be in the wrong place)</additional_instructions>
If the user asks you to "ask someone" / "run it by someone", ONLY THEN add that user to the approvers list (with required set to true)
ONLY if the user asks you to notify someone, then add that user to the approvers list (with required set to false).
Use your discretion to determine whether the user is asking you to notify someone or ask them for permission / run it by someone.
Do not add ANY information that isn't in the request. If the user doesn't specify something, leave it blank.
"""
        logger.info("Calling GPT-4o to parse event request")
        _time = time.time()
        response = await self.openai_client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that can parse event requests.",
                },
                {"role": "user", "content": prompt},
            ],
            response_format=SmartParseEvent,
        )
        logger.info(f"Parsed event request in {time.time() - _time:.2f} seconds")
        cost = self._calculate_cost(response)
        logger.info(
            f"Cost - Input: ${cost.input_cost:.6f}, Output: ${cost.output_cost:.6f}, Total: ${cost.total_cost:.6f}"
        )
        _object = response.choices[0].message.parsed

        # ensure that the start/end date isn't timezone aware
        if _object and hasattr(_object, 'start_date') and _object.start_date and hasattr(_object.start_date, 'date_time') and _object.start_date.date_time:
            _object.start_date.date_time = _object.start_date.date_time.replace(
                tzinfo=None
            )
        if _object and hasattr(_object, 'end_date') and _object.end_date and hasattr(_object.end_date, 'date_time') and _object.end_date.date_time:
            _object.end_date.date_time = _object.end_date.date_time.replace(tzinfo=None)
        return _object

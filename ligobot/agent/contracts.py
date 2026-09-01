from collections.abc import Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Any, Literal
from .template.prompt import llm_response_schema
from .tools.registry import tool_defs


@dataclass
class ChatRequest:
    messages: list
    tools: list
    ...


class LLMProvider(ABC):
    def __init__(self):
        # self.response_schema = llm_response_schema
        self.tools = tool_defs

    @abstractmethod
    def chat(self, system_prompt, message) -> Any:
        pass

    @abstractmethod
    def stream_chat(self, message, callback: Callable[[Any]]) -> Any:
        pass

    @abstractmethod
    def end_chat(self):
        pass


class ToolCall(BaseModel):
    function_name: str
    function_arguments: dict[str, Any]


class ChatResponse(BaseModel):
    response_type: Literal["text", "tool_call"]
    text_output: str
    tool_call: ToolCall | None = None

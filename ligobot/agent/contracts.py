from collections.abc import Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Any, Literal, Optional
from .template.prompt import llm_response_schema
from .tools.registry import tool_defs
from sqlalchemy import Column, Integer, func
from sqlalchemy.types import Enum, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


@dataclass
class ChatRequest:
    messages: list
    tools: list
    ...


class LLMProvider(ABC):
    name = ""

    def __init__(self):
        # self.response_schema = llm_response_schema
        self.tools = tool_defs

    @abstractmethod
    def chat(self, system_prompt, messages) -> Any:
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


class ResponseError(BaseModel):
    message: str
    body: Any = None
    code: str | None = None


class ChatResponse(BaseModel):
    response_type: Literal["text", "tool_call", "error"]
    text_output: str = ""
    tool_call: ToolCall | None = None
    error: ResponseError | None = None


class History(Base):
    __tablename__ = "conv_history"

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, index=True, default=1)

    role = Column(Enum("user", "llm"), nullable=False)
    message = Column(Text, nullable=False)
    response_type = Column(Enum("text", "tool_call"), nullable=False)

    created_at = Column(DateTime, index=True, server_default=func.now(), nullable=False)

    def __repr__(self):
        return (
            f"History(id={self.id}, role={self.role}, "
            f"created_at={self.created_at}, message={self.message}, "
            f"response_type={self.response_type}, conversation_id={self.conversation_id})"
        )

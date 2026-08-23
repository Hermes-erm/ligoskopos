from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class ChatRequest:
    messages: list
    tools: list
    ...


class LLMProvider(ABC):

    @abstractmethod
    def chat(self, message: str) -> Any:
        pass

    @abstractmethod
    def stream_chat(self, message: str) -> Any:
        pass

    @abstractmethod
    def end_chat(self):
        pass

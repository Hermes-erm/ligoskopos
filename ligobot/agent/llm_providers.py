import httpx
from typing import Any
from google import genai
from openai import OpenAI as openai
from config import GEMINI_API_KEY, OPENROUTER_API_KEY
from agent.contracts import LLMProvider, ChatResponse


class Gemini(LLMProvider):
    name = "Gemini"

    def __init__(self, model: str):
        super().__init__()
        self.models = ["gemini-3.5-flash-lite", "gemini-3.7-flash", "gemini-3.5-flash"]
        self.model = model
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def chat(self, system_prompt, message):
        interaction = self.client.interactions.create(
            model=self.model,
            system_instruction=system_prompt,
            input=message,
            tools=self.tools,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": ChatResponse.model_json_schema(),
            },
        )
        return interaction

    def stream_chat(self, messages, callback):
        stream = self.client.interactions.create(
            model=self.model, input=messages, stream=True
        )

        for event in stream:
            if event.event_type == "step.delta":
                if event.delta.type == "text":
                    callback(event.delta.text)

    def end_chat(self):
        return super().end_chat()


class OpenRouter(LLMProvider):  # OpenAI SDK under OpenRouter
    name = "openrouter"

    def __init__(self, model: str):
        super().__init__()
        self.models = [
            "nvidia/nemotron-3.5-lightning:free",
            "nvidia/nemotron-3-super-120b-a12b:free",
            "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
        ]
        self.model = model
        self.client = openai(
            base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY
        )

    def chat(self, system_prompt, message):
        interaction = self.client.responses.parse(
            model=self.model,
            instructions=system_prompt,
            input=message,
            tools=self.tools,
            text_format=ChatResponse,
        )
        return interaction

    def stream_chat(self, messages, callback):
        stream = self.client.responses.create(
            model=self.model,
            input=[{"role": "user", "content": f"{messages}"}],
            stream=True,
        )

        for event in stream:
            # response.reasoning_text.delta
            if event.type == "response.output_text.delta":
                callback(event.delta)

    def end_chat(self):
        return super().end_chat()

from typing import Any
from google import genai
from openai import OpenAI
from config import GEMINI_API_KEY, OPENROUTER_API_KEY, GROQ_API_KEY
from agent.contracts import LLMProvider, ChatResponse


class Gemini(LLMProvider):
    name = "Gemini"
    models = ["gemini-3.5-flash-lite", "gemini-3.7-flash", "gemini-3.5-flash"]

    def __init__(self, model: str = models[0]):
        super().__init__()
        self.model = model
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def chat(self, system_prompt, message):
        interaction = self.client.interactions.create(
            model=self.model,
            system_instruction=system_prompt,
            input=message,
            # tools=self.tools,
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


class OpenAICompatible(LLMProvider):
    name = "openrouter"

    def __init__(self, name, active_model, models, base_url, api_key):
        super().__init__()

        self.name = name
        self.model = active_model
        self.models = models
        self.client = OpenAI(base_url=base_url, api_key=api_key)

    def chat(self, system_prompt, message):
        interaction = self.client.responses.create(
            model=self.model,
            instructions=system_prompt,
            input=message,
            # tools=self.tools,
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


class OpenRouter(OpenAICompatible):
    name = "openrouter"
    models = [
        "nvidia/nemotron-3.5-lightning:free",
        "nvidia/nemotron-3-super-120b-a12b:free",
        "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    ]

    def __init__(self, model: str = models[0]):

        super().__init__(
            name=self.name,
            active_model=model,
            models=self.models,
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        )


class Groq(OpenAICompatible):
    name = "groq"
    models = [
        "qwen/qwen3.6-27b",
        "qwen/qwen3.8-27b",
        "openai/gpt-oss-20b",
        "openai/gpt-oss-120b",
    ]

    def __init__(self, model: str = models[0]):

        super().__init__(
            name=self.name,
            active_model=model,
            models=self.models,
            base_url="https://api.groq.com/openai/v1",
            api_key=GROQ_API_KEY,
        )

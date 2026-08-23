from google import genai
from openai import OpenAI as openai
from contracts import LLMProvider
from config import GEMINI_API_KEY, OPENAI_API_KEY


class LLMClient:
    """
    The llm interface is the interface engine.
    Model agnostic

    It:
    1. Receives messages from the Loop
    2. stage context to selective model
    3. Calls the LLM
    4. Sends responses back to Loop engine
    """

    def __init__(self, provider: LLMProvider):
        self.provider = provider
        self.token_limit = None
        self.token_used = None

    def generate(self, message: str):  # return agent structured response
        response = self.provider.chat(message)
        return response


class Gemini(LLMProvider):
    name = "Gemini"

    def __init__(self, model: str):
        self.models = ["gemini-3.5-flash-lite", "gemini-3.7-flash", "gemini-3.5-flash"]
        self.model = model
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def chat(self, message: str):
        interaction = self.client.interactions.create(model=self.model, input=message)
        return interaction.output_text

    def stream_chat(self, message, callback):
        stream = self.client.interactions.create(
            model=self.model, input=message, stream=True
        )

        for event in stream:
            if event.event_type == "step.delta":
                if event.delta.type == "text":
                    callback(event.delta.text)

    def end_chat(self):
        return super().end_chat()


# Hold for now
class OpenAI(LLMProvider):
    name = "OpenAI"

    def __init__(self, model="gpt-4o-mini"):
        self.models = ["gpt-oss-120b", "gpt-4o-2024-08-06", "gpt-5.5-2026-04-23"]
        self.model = model
        self.client = openai(api_key=OPENAI_API_KEY)

    def chat(self, message: str):
        interaction = self.client.responses.create(model=self.model, input=message)
        print(interaction.output_text)

    def stream_chat(self, message):
        stream = self.client.responses.create(
            model="gpt-5.5", input=message, stream=True
        )

        for event in stream:
            print(event)
        # if event.event_type == "step.delta":
        # if event.delta.type == "text":
        #     print(event.delta, end="", flush=True)

    def end_chat(self):
        return super().end_chat()

from agent.contracts import LLMProvider


class LLMClient:
    """
    Model-agnostic interface between the agent loop and an LLM provider.

    Responsibilities:
    1. Receive context/messages from the agent loop.
    2. Delegate requests to the configured LLM provider.
    3. Return generated responses to the agent loop.
    """

    def __init__(self, provider: LLMProvider):
        self.provider = provider
        self.token_limit = None
        self.token_used = None

    def generate(self, messages: str):  # return agent structured response
        response = self.provider.chat(messages)
        return response

    def stream(self, messages, on_chunk):
        self.provider.stream_chat(messages, on_chunk)

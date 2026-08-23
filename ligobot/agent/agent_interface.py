from agent.llm_client import LLMClient


class Agent:
    """
    1. Agent
        1. LLM call
        2. Context building
        3. Memory
            1. MEMORY.md
            2. SOUL.md
            3. USER.md
        4. Tool execution
        5. History
    """

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def _process_stream_data(self, message):
        print(message, end="", flush=True)

    def run(self, user_prompt: str): ...

    def _loop(self): ...


# run(): self.llm_client.provider.stream_chat(user_prompt, self._process_stream_data)

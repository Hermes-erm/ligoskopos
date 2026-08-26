import json
from agent.tools.registry import tool_defs
from agent.llm_client import LLMClient


class Agent:
    """
    Coordinates the agent's core execution flow.

        1. Build the context for the LLM.
        2. Send prompts to the configured LLM client.
        3. Manage conversation and long-term memory.
            1. MEMORY.md
            2. SOUL.md
            3. USER.md
        4. Execute tools requested by the LLM.
        5. Maintain conversation history.
    """

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def _process_stream_data(self, chunk):
        print(chunk, end="", flush=True)

    def run(self, user_prompt: str):
        message = {"tools": tool_defs, "user_prompt": user_prompt}
        print(json.dumps(message))
        res = self.llm_client.generate(json.dumps(message))
        print(res)

    def _build_context(self): ...

    def _loop(self): ...


# run(): self.llm_client.provider.stream_chat(user_prompt, self._process_stream_data)

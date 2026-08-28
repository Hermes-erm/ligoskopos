import json
from agent.tools.registry import tool_defs
from agent.llm_client import LLMClient
from .context_builder import ContextBuilder


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

    def __init__(self, llm_client: LLMClient, context_builder: ContextBuilder):
        self.llm_client = llm_client
        self.context_builder = context_builder
        self.tools = tool_defs

    def _process_stream_data(self, chunk):
        print(chunk, end="", flush=True)

    def run(self, user_prompt: str):
        # message = self.context_builder.build(user_prompt)
        instruction = self.context_builder.system_prompt
        response = self.llm_client.generate(instruction, user_prompt)

    def _loop(self): ...


# run(): self.llm_client.provider.stream_chat(user_prompt, self._process_stream_data)

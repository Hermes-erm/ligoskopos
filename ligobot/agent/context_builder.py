from typing import Any
import json
from .template.prompt import soul, agent, user, memory, response, llm_response_schema
from .tools.registry import tool_defs


class ContextBuilder:
    def __init__(self):
        self.agent_profile = agent
        self.agent_personality = soul
        self.user_context = user
        self.memory_context = memory
        self.response_schema = response

        self._generate_system_prompt(
            self.agent_personality,
            self.agent_profile,
            self.user_context,
            self.memory_context,
            self.response_schema,
        )

    def _generate_system_prompt(self, *args):
        self.system_prompt = "\n".join(args)
        self.system_prompt += f"\n{json.dumps(llm_response_schema)}"
        self.system_prompt += (
            "\n\n## Available Tools\n"
            "Use the following tools when necessary. "
            "Select a tool by its exact `name` and provide only the arguments defined in its `parameters`.\n\n"
            f"{json.dumps(tool_defs)}"
        )

        return self.system_prompt

    def build(self, message: str): ...

    def update(self):  # Update dynamically on run-time
        ...

from typing import Any
from .template.prompt import soul, agent, user, memory


class ContextBuilder:
    def __init__(self):
        self.agent_soul = f"\n{soul}\n"
        self.agent = f"\n{agent}\n"
        self.user = f"\n{user}\n"
        self.agent_memory = f"\n{memory}\n"
        self.system_prompt: str = """"""

        self._generate_system_prompt(
            self.agent_soul, self.agent, self.user, self.agent_memory
        )

    def _generate_system_prompt(self, *args):
        self.system_prompt = "\n".join(args)
        return self.system_prompt

    def build(self, message: str):
        messages = []
        messages.append(
            {
                "type": "Agent-Instructions",
                "desc": "Information about the agent",
                "content": self.agent,
            }
        )
        messages.append(
            {
                "type": "Agent-Personality",
                "desc": "The agent's personality, values, and behavioral guidelines",
                "content": self.agent_soul,
            }
        )
        messages.append(
            {
                "type": "About-User",
                "desc": "Information and context about the user",
                "content": self.user,
            }
        )
        messages.append(
            {
                "type": "About-Memory",
                "desc": "Relevant memories and past context",
                "content": self.agent_memory,
            }
        )
        messages.append(
            {
                "type": "User-Prompt",
                "desc": "The user's current request",
                "content": message,
            }
        )

        return messages

    def update(self):  # Update dynamically on run-time
        ...

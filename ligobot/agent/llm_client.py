import json_repair
from .contracts import ChatResponse
from agent.contracts import LLMProvider
from agent.llm_providers import Gemini, OpenRouter, Groq
from prompt_toolkit.shortcuts import choice


class LLMClient:
    """
    Model-agnostic interface between the agent loop and an LLM provider.

    Responsibilities:
    1. Receive context/messages from the agent loop.
    2. Delegate requests to the configured LLM provider.
    3. Return generated responses to the agent loop.
    """

    providers = [
        {
            "provider": Groq,
            "desc": "Groq (default)",
            "default_model": "qwen/qwen3.6-27b",
        },
        {
            "provider": Gemini,
            "desc": "Gemini",
            "default_model": "gemini-3.5-flash-lite",
        },
        {
            "provider": OpenRouter,
            "desc": "Openrouter - nvidia/nemotron",
            "default_model": "nvidia/nemotron-3.5-lightning:free",
        },
    ]

    def __init__(self):

        options = [
            (ind, self.providers[ind]["desc"]) for ind in range(len(self.providers))
        ]
        provider_ind = choice(
            message="Choose the provider:", options=options, default=options[0]
        )
        selected_provider = self.providers[provider_ind]

        self.provider = selected_provider["provider"](
            selected_provider["default_model"]
        )

        self.token_limit = None
        self.token_used = None

    def generate(self, system_prompt, message):
        response = self.provider.chat(system_prompt, message)
        # print(response)
        data = json_repair.loads(response.output_text)
        # print("*" * 100)
        # print(response.output, sep=f"\n {'*' * 100} \n")
        return ChatResponse.model_validate(data)  # Python dict/instance -> Schema

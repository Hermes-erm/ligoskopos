import json_repair
from .contracts import ChatResponse, History
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
            "default_model": "openai/gpt-oss-20b",
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

    def __init__(self, provider: LLMProvider | None = None):

        if provider:
            self.provider = provider
        else:
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

    def generate(self, system_prompt, history, user_req):
        messages = self._build_conv(history, user_req)

        response = self.provider.chat(system_prompt, messages)
        # print(response)

        data = json_repair.loads(response)
        if not isinstance(data, dict):  # Handle on err log
            print(repr(data))
            raise ValueError(
                f"Model did not return valid JSON. Raw output: {response!r}"
            )
        return ChatResponse.model_validate(data)  # Python dict/instance -> Schema

    def _build_conv(self, history: list[History], user_req: str):
        convs = "### Chat History ###\n"

        for msg in history:
            convs += f"[{msg.created_at}] {msg.role}: {msg.message}\n"

        convs += f"\n### Current User Query ###\n{user_req}"

        return convs


# [
#     [
#         {
#             "type": "user_input",
#             "content": [{"type": "text", "text": "Hello!"}],
#         },
#         {
#             "type": "model_output",
#             "content": [
#                 {
#                     "type": "text",
#                     "text": "Hi there! How can I help you today?",
#                 }
#             ],
#         },
#         {
#             "type": "user_input",
#             "content": [
#                 {
#                     "type": "text",
#                     "text": "What is the capital of France?",
#                 }
#             ],
#         },
#     ]
# ]

# [
#     {"role": "user", "content": "i like blue"},
#     {"role": "assistant", "content": "i like orange"},
#     {"role": "user", "content": message},
# ]

# Make it work first, structure it later
from pathlib import Path


def load_file(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


WORKSPACE_DIR = Path(__file__).resolve().parent / "workspace"

soul = load_file(WORKSPACE_DIR / "SOUL.md")
agent = load_file(WORKSPACE_DIR / "AGENTS.md")
user = load_file(WORKSPACE_DIR / "USER.md")
memory = load_file(WORKSPACE_DIR / "MEMORY.md")
response = load_file(WORKSPACE_DIR / "RESPONSE.md")

llm_response_schema = {
    "type": "json_schema",
    "name": "llm_response",
    "strict": False,
    "schema": {
        "type": "object",
        "properties": {
            "response_type": {
                "type": "string",
                "enum": ["text", "tool_call"],
                "description": ("The type of response produced by the LLM."),
            },
            "text_output": {
                "type": "string",
                "description": (
                    "The textual response. Use an empty string when "
                    "response_type is 'tool_call'."
                ),
            },
            "tool_call": {
                "type": "object",
                "description": (
                    "The tool call to execute when response_type is 'tool_call'."
                ),
                "properties": {
                    "function_name": {
                        "type": "string",
                    },
                    "function_arguments": {
                        "type": "string",
                    },
                },
                "required": [
                    "function_name",
                    "function_arguments",
                ],
                "additionalProperties": False,
            },
        },
        "required": [
            "response_type",
            "text_output",
            "tool_call",
        ],
        "additionalProperties": False,
    },
}

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
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "response_type": {
                "type": "string",
                "enum": ["text", "tool_call"],
            },
            "text_output": {
                "type": "string",
            },
            "tool_call": {
                "anyOf": [
                    {
                        "type": "object",
                        "properties": {
                            "function_name": {"type": "string"},
                            "function_arguments": {"type": "object"},
                        },
                        "required": [
                            "function_name",
                            "function_arguments",
                        ],
                        "additionalProperties": False,
                    },
                    {"type": "null"},
                ],
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

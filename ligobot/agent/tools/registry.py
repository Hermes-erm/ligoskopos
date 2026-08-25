import inspect
import json
from typing import Callable, Any, Dict

tools: list[Dict[str, Any]] = []


def register(*args, **kwargs):
    # Handle decorator accepted arguments
    tool_info = {
        "type": "function",
        "description": kwargs.get("desc"),
        "parameters": {
            "type": "object",
            "properties": {},  # "customer_id": {"type": "string"}
            "required": [],
        },
    }

    def extract_func(func: Callable):
        # Handle func metadata extraction
        tool_info["function"] = func
        tool_info["name"] = func.__name__

        sig = inspect.signature(func)
        required = []

        for name, param in sig.parameters.items():
            tool_info["parameters"]["properties"][name] = {
                "type": param.annotation,
                "default_value": param.default,
            }
            if param.annotation is inspect.Parameter.empty:
                required.append(name)

        tool_info["parameters"]["required"] = required
        tools.append(tool_info)

        def wrapper(*args, **kwargs):
            # Handle function execution
            return func(*args, **kwargs)

        return wrapper

    return extract_func

import json
import inspect
from typing import Callable, Any, Dict

tool_defs: list[Dict[str, Any]] = []
tool_functions: Dict[str, Callable] = {}


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
        tool_functions[func.__name__] = func
        tool_info["name"] = func.__name__

        sig = inspect.signature(func)

        required = kwargs.get("required", [])
        tool_info["parameters"]["properties"] = kwargs.get("properties", {})

        # TODO: Re-enable automatic parameter schema generation later
        # for name, param in sig.parameters.items():
        #     property_schema = {"type": _json_type(param.annotation)}

        #     if param.default is inspect.Parameter.empty:
        #         required.append(name)
        #     else:
        #         property_schema["default"] = param.default

        #     tool_info["parameters"]["properties"][name] = property_schema

        tool_info["parameters"]["required"] = required
        tool_defs.append(tool_info)

        def wrapper(*args, **kwargs):
            # Handle function execution
            return func(*args, **kwargs)

        return wrapper

    return extract_func


def _json_type(annotation):
    if annotation == str:
        return "string"
    if annotation == int:
        return "integer"
    if annotation == float:
        return "number"
    if annotation == bool:
        return "boolean"
    if annotation == list[str]:
        return "array[string]"
    return "string"

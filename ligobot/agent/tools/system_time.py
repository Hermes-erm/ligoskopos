import json
from datetime import datetime
from registry import register


@register(
    desc="""Returns the system’s current local date and time along with the associated timezone name. The tool uses the system timezone to produce a timezone-aware timestamp, making it suitable for applications that need reliable local time and timezone information.
"""
)
def _get_system_time(arg_a, agr_b: list[int] = [1, 2], arg_c: str = "val_2"):
    # Get local time with system timezone details attached
    aware_local = datetime.now().astimezone()

    res = {
        "timezone_aware_local_time": f"{aware_local}",
        "timezone_name": aware_local.tzname(),
    }

    return json.dumps(res)

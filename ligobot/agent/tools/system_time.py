from datetime import datetime
import json


# @tool()
def _get_system_time():
    # Get local time with system timezone details attached
    aware_local = datetime.now().astimezone()

    res = {
        "timezone_aware_local_time": f"{aware_local}",
        "timezone_name": aware_local.tzname(),
    }

    return json.dumps(res)

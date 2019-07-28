import json
from typing import Dict


def error_to_json(error: str) -> Dict:
    return json.loads(error.replace("400: ", ""))

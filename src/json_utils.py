import json
from typing import Dict

def get_json(file_info):
    try:
        with file_info.open("r", encoding="utf-8") as usf:
            return json.load(usf)  # what does load?
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_data(file, arguments: Dict) -> None:
    with file.open("w") as fp:
        json.dump(arguments, fp)
from typing import Dict
from urllib.parse import parse_qs


def linearize_qs(qs: Dict) -> Dict:
    """
    Linearizes qs dict: only the first value is populated into result
    """
    result = {}

    for key, values in qs.items():
        if not values:
            continue

        value = values
        if isinstance(values, list):
            value = values[0]

        result[key] = value

    return result


def parse_function(request):
    _path, *qs = request.path.split("?")
    arguments = {}

    if len(qs) != 1:
        return arguments

    qs = qs[0]
    qs = parse_qs(qs)

    for keys, values in qs.items():
        if not values:
            continue
        arguments[keys] = values[0]

    return arguments


def age_calculating(qs_arguments: Dict):
    age = qs_arguments.get("age")
    if age is None:
        return age
    return int(age)


def name_calculating(qs_arguments: Dict):
    return qs_arguments.get("name", "anonymous")


def path_calculating(path1):
    path = path1.split("?")[0]
    if path[-1] == "/":
        path = path[:-1]
    return path

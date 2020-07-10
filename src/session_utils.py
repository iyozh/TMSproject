import os
from typing import Dict
from urllib.parse import parse_qs

from src.json_utils import get_json, save_data


def parse_user_sessions(headers, rfile) -> Dict[str, str]:
    content_length = int(headers["Content-Length"])
    data = rfile.read(content_length)
    payload = data.decode()
    qs = parse_qs(payload)
    user_data = {}

    for key, values in qs.items():
        if not values:
            continue
        user_data[key] = values[0]

    return user_data


def get_request_payload(headers, rfile) -> str:
    try:
        content_length = int(headers[("content-length")])
        payload = rfile.read(content_length)
    except (KeyError, ValueError):
        payload = ""
    return payload.decode()


def get_session_id(headers):
    cookie = headers.get("Cookie")
    if not cookie:
        return {}
    return cookie


def load_user_session(headers, file_name):
    session_id = get_session_id(headers)
    if not session_id:
        return {}
    session = get_json(file_name)
    return session.get(session_id, {})


def save_user_session(headers, session, file_name):
    session_id = get_session_id(headers) or os.urandom(16).hex()
    sessions = get_json(file_name)
    sessions[session_id] = session
    save_data(file_name, sessions)

    return session_id
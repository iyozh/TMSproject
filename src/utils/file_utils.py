from pathlib import Path

from errors import NotFound


def get_picture(file_name: Path):
    if not file_name.is_file():
        raise NotFound()

    with file_name.open("rb") as picture:
        image = picture.read()

    return image


def get_content(file_name: Path):
    if not file_name.is_file():
        raise NotFound()

    with file_name.open("r") as fp:
        content = fp.read()

    return content


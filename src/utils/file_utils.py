from pathlib import Path

from django.http import Http404, HttpResponse

from errors import NotFound
from path import PORTFOLIO


def get_picture(file_name: Path):
    if not file_name.is_file():
        raise NotFound()

    with file_name.open("rb") as picture:
        image = picture.read()

    return image


def get_content(file_name: Path):
    if not file_name.is_file():
        raise NotFound()

    with file_name.open("r", encoding="utf-8") as fp:
        content = fp.read()

    return content


def img_handler(request, **kw):
    path_to_file = kw["path_to_file"]
    image_dir = PORTFOLIO / "img"
    real_image = image_dir / path_to_file

    if not real_image.is_file():
        raise Http404("I cant find image:(")

    with real_image.open("rb") as fp:
        image = fp.read()

    image_format = real_image.suffix[1:].lower()

    if image_format == "jpg":
        image_format = "jpeg"

    return HttpResponse(image, f"image/{image_format}")


def css_handler(request, **kw):
    path_to_file = kw["path_to_file"]
    real_css_dir = PORTFOLIO / "css" / path_to_file

    if not real_css_dir.is_file():
        raise Http404("I cant find css-file:(")

    with real_css_dir.open("r") as fp:
        css = fp.read()

    return HttpResponse(css, "text/css")

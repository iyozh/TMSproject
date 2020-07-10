import os
import socketserver
from http.server import SimpleHTTPRequestHandler

from src.pages.education import edu_handler
from src.errors import Missing_Data, NotFound
from src.utils.file_utils import get_picture
from src.pages.goodbye import get_page_goodbye
from src.pages.hello import handler_hello
from src.path import PROJECT_DIR
from src.pages.projects import get_projects
from src.responses import respond_400, respond_404
from src.pages.resume import get_portfolio
from src.pages.stats import get_stats
from src.pages.test_projects import get_editing_page, projects_handler
from src.pages.theme_page import theme_handler
from src.utils.utils import path_calculating

PORT = int(os.getenv("PORT", 8000))
print(f"PORT = {PORT}")


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            self.do("get")
        except NotFound:
            file_name = PROJECT_DIR / "images" / "error404.jpg"
            image = get_picture(file_name)
            respond_404(self, image, "image/jpeg")

    def do_POST(self):
        try:
            self.do("post")
        except NotFound:
            file_name = PROJECT_DIR / "images" / "error404.jpg"
            image = get_picture(file_name)
            respond_404(image, "image/jpeg")

    def do(self, method: str):
        default_handler = super().do_GET
        path = path_calculating(self.path)
        handlers = {
            "/hello": handler_hello,
            "/goodbye": get_page_goodbye,
            "/aboutme": get_portfolio,
            "/projects": get_projects,
            "/education": edu_handler,
            "/education/night_mode": edu_handler,
            "/theme": theme_handler,
            "/theme/night_mode": theme_handler,
            "/counter": get_stats,
            "": default_handler,
            "/test_projects": projects_handler,
            "/test_projects/editing": get_editing_page,
            "/test_projects/editing/add": projects_handler,
            "/test_projects/editing/delete": projects_handler,
            "/test_projects/editing/change": projects_handler,
        }

        if path.startswith("/portfolio"):
            default_handler()
            return

        if path not in handlers:
            raise NotFound()

        handler = handlers.get(path)

        try:
            if handler is default_handler:
                handler()
            else:
                handler(self, method, path)
        except NotFound:
            file_name = PROJECT_DIR / "images" / "error404.jpg"
            image = get_picture(file_name)
            respond_404(self, image, "image/jpeg")
        except Missing_Data:
            respond_400(self)


with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("it works")
    httpd.serve_forever()

import os
import socketserver
from datetime import datetime
from http.server import SimpleHTTPRequestHandler
from typing import Dict
from urllib.parse import parse_qs
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent.resolve()
print(f"PROJECT_DIR = {PROJECT_DIR}")

PORTFOLIO = PROJECT_DIR / "portfolio"
print(f"PORTFOLIO = {PORTFOLIO}")

year = datetime.now().year
hour = datetime.now().hour

PORT = int(os.getenv("PORT", 8000))
print(f"PORT = {PORT}")


class NotFound(Exception):
    ...


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path = self.path_calculating()
        handlers = {"/hello": self.hello_response,
                    "/goodbye": self.goodbye_response,
                    "/aboutme": self.aboutme_response,
                    "/projects": self.projects_response,
                    "/education": self.education_response
                    }
        handler = handlers.get(path, super().do_GET)
        try:
            handler()
        except NotFound:
            file_name = PROJECT_DIR / "images" / "error404.jpg"
            content = self.get_content(file_name)
            self.response(content, status_code=404, content_type="image/jpeg")

    def hello_response(self):
        arguments = self.parse_function()
        path = self.path_calculating()
        name = self.name_calculating(arguments)
        age = self.age_calculating(arguments)
        msg = f"""
                                    Hello {name}!                

                                    Your path: {path}

                                                       """
        if age:
            born = year - age
            msg += f"\n\t\t\t\t   You were born in {born}"

        self.response(msg)

    def goodbye_response(self):
        if hour in range(6, 11):
            msg = f"\n\t\t\t\t   Good morning!"
        elif hour in range(12, 24):
            msg = f"\n\t\t\t\t   Good day!"
        else:
            msg = f"\n\t\t\t\t   Good night!"

        self.response(msg)

    def education_response(self):
        file_name = PORTFOLIO / "education" / "index1.html"
        content = self.get_content(file_name)
        self.response(content, content_type="text/html")

    def aboutme_response(self):
        file_name = PORTFOLIO / "aboutme" / "index.html"
        content = self.get_content(file_name)
        self.response(content, content_type="text/html")

    def projects_response(self):
        file_name = PORTFOLIO / "projects" / "index.html"
        content = self.get_content(file_name)
        self.response(content, content_type="text/html")

    def get_content(self, file_name: Path):
        if not file_name.is_file():
            raise NotFound()

        with file_name.open("rb") as project_file:
            content = project_file.read()

        return content

    def path_calculating(self):
        path = self.path.split("?")[0]
        if path[-1] == "/":
            path = path[:-1]
        return path

    def name_calculating(self, qs_arguments: Dict):
        return qs_arguments.get("name", "anonymous")

    def age_calculating(self, qs_arguments: Dict):
        return int(qs_arguments.get("age", 0))

    def parse_function(self):
        _path, *qs = self.path.split("?")
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

    def response(self, msg, status_code=200, content_type="text/plain"):
        self.send_response(status_code)
        self.send_header("Content-type", content_type)
        self.send_header("Content-length", str(len(msg)))
        self.end_headers()

        if isinstance(msg, str):
            self.wfile.write(msg.encode())
        self.wfile.write(msg)

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("it works")
    httpd.serve_forever()

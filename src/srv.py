import json
import os
import socketserver
from datetime import datetime
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from typing import Dict
from urllib.parse import parse_qs

PROJECT_DIR = Path(__file__).parent.parent.resolve()
print(f"PROJECT_DIR = {PROJECT_DIR}")

PORTFOLIO = PROJECT_DIR / "portfolio"
print(f"PORTFOLIO = {PORTFOLIO}")

EDUCATION = PORTFOLIO / "education" / "education.json"

COUNTER = PROJECT_DIR / "counters.json"

THEME = PROJECT_DIR / "theme.json"

year = datetime.now().year
hour = datetime.now().hour

PORT = int(os.getenv("PORT", 8000))
print(f"PORT = {PORT}")


class NotFound(Exception):
    ...


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.do()
    #
    # def do_POST(self):
    #     try:
    #         self.do('post')
    #     except NotFound:
    #         file_name = PROJECT_DIR / "images" / "error404.jpg"
    #         content = self.get_content(file_name)
    #         self.response(content, status_code=404, content_type="image/jpeg")

    def do(self):
        path = self.path_calculating()
        handlers = {
            "/hello": self.hello_response,
            "/goodbye": self.goodbye_response,
            "/aboutme": self.aboutme_response,
            "/projects": self.projects_response,
            "/education": self.education_response,
            "/counter": self.counter_response,
        }
        handler = handlers.get(path, super().do_GET)
        try:
            handler()
        except NotFound:
            file_name = PROJECT_DIR / "images" / "error404.jpg"
            content = self.get_picture(file_name)
            self.response(content, status_code=404, content_type="image/jpeg")
    #
    # def choose_theme(self):
    #     path = self.path_calculating()
    #     switcher = {
    #         "/black_theme": self.black_theme
    #     }
    #     switcher = switcher[path]
    #     switcher()
    #
    # def black_theme(self):
    #     arguments = self.get_json(THEME)
    #     file_name = PORTFOLIO / "stats" / "index.html"
    #     black_theme = arguments["black_theme"]
    #     content = self.get_content(file_name).format(black_theme=black_theme)
    #     self.response(content, content_type="text/html")


    def hello_response(self):
        self.visits_counter()
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

    def visits_counter(self):
        arguments = self.get_json(COUNTER)
        path = self.path_calculating()
        arguments[path] = arguments[path] + 1
        self.save_data(arguments)

    def goodbye_response(self):
        self.visits_counter()
        if hour in range(6, 11):
            msg = f"\n\t\t\t\t   Good morning!"
        elif hour in range(12, 24):
            msg = f"\n\t\t\t\t   Good day!"
        else:
            msg = f"\n\t\t\t\t   Good night!"

        self.response(msg)

    def education_response(self):
        arguments = self.get_json(EDUCATION)
        univer = arguments["univer"]
        major = arguments["major"]
        qualification = arguments["qualification"]
        start = arguments["start"]
        end = arguments["end"]

        msg = f"""                          EDUCATION:{univer}
                          Major:{major}
                          Qualification:{qualification}
                          Start:{start}
                          End:{end}
               """

        self.response(msg)

    def counter_response(self):
        arguments = self.get_json(COUNTER)
        hello = arguments["/hello"]
        goodbye = arguments["/goodbye"]
        file_name = PORTFOLIO / "stats" / "index.html"
        content = self.get_content(file_name).format(greetings=hello, partings=goodbye)
        self.response(content, content_type="text/html")
        # if method == 'post':
        #     self.choose_theme()

    def aboutme_response(self):
        file_name = PORTFOLIO / "aboutme" / "index.html"
        content = self.get_content(file_name)
        self.response(content, content_type="text/html")

    def projects_response(self):
        file_name = PORTFOLIO / "projects" / "index.html"
        content = self.get_content(file_name)
        self.response(content, content_type="text/html")

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

    def get_json(self, file_info):
        with file_info.open("r") as fp:
            arguments = json.load(fp)
        return arguments

    def get_content(self, file_name: Path):
        if not file_name.is_file():
            raise NotFound()

        with file_name.open("r") as project_file:
            content = project_file.read()

        return content

    def get_picture(self, file_name: Path):
        if not file_name.is_file():
            raise NotFound()

        with file_name.open("rb") as picture:
            content = picture.read()

        return content
    def save_data(self, arguments) -> None:
        with COUNTER.open("w") as fp:
            json.dump(arguments, fp)

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

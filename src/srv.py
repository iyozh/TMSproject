import json
import os
import socketserver
from datetime import datetime
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from typing import Dict
from urllib.parse import parse_qs
from http import cookies

PROJECT_DIR = Path(__file__).parent.parent.resolve()
print(f"PROJECT_DIR = {PROJECT_DIR}")

PORTFOLIO = PROJECT_DIR / "portfolio"
print(f"PORTFOLIO = {PORTFOLIO}")

EDUCATION = PORTFOLIO / "education" / "education.json"

COUNTER = PROJECT_DIR / "data" / "counters.json"

THEME = PROJECT_DIR / "data" / "theme.json"

THEME_INDEX = PORTFOLIO / "theme" / "index.html"

SESSION = PROJECT_DIR / "data" / "session.json"

year = datetime.now().year
hour = datetime.now().hour

PORT = int(os.getenv("PORT", 8000))
print(f"PORT = {PORT}")



class NotFound(Exception):
    ...


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            self.do('get')
        except NotFound:
            file_name = PROJECT_DIR / "images" / "error404.jpg"
            image = self.get_picture(file_name)
            self.respond_404(image, "image/jpeg")

    def do_POST(self):
        try:
            self.do('post')
        except NotFound:
            file_name = PROJECT_DIR / "images" / "error404.jpg"
            image = self.get_picture(file_name)
            self.respond_404(image, "image/jpeg")

    def do(self, method: str):
        default_handler = super().do_GET
        path = self.path_calculating()
        handlers = {
            "/hello": self.handler_hello,
            "/goodbye": self.goodbye_response,
            "/aboutme": self.aboutme_response,
            "/projects": self.projects_response,
            "/education": self.education_response,
            "/theme": self.theme_handler,
            "/counter": self.counter_response,
            "": default_handler
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
                handler(method, path)
        except NotFound:
            file_name = PROJECT_DIR / "images" / "error404.jpg"
            image = self.get_picture(file_name)
            self.respond_404(image, "image/jpeg")

    def handler_hello(self, method: str, path):
        self.visits_counter(path)
        switcher = {
            'get': self.hello_GETresponse,
            'post': self.hello_POSTresponse
        }
        switcher = switcher[method]
        switcher(path)


    def hello_GETresponse(self,path):
        sessions = self.load_user_session() or self.parse_function()
        name = self.name_calculating(sessions)
        age = self.age_calculating(sessions)
        born = None
        if age:
            born = year - age

        html_content = PROJECT_DIR / "hello" / "hello.html"
        hello_page = self.get_content(html_content).format(name=name, year=born)
        self.respond_200(hello_page, "text/html")


    def hello_POSTresponse(self,path):
        form = self.parse_user_sessions()
        session = self.load_user_session()
        session.update(form)
        session_id = self.save_user_session(session)
        # self.save_data(SESSION, session)
        self.respond_302("/hello",session_id)

    def load_user_session(self):
        session_id = self.get_session_id()
        if not session_id:
            return {}
        session = self.get_json(SESSION)
        return session.get(session_id, {})

    def save_user_session(self, session):
        session_id = self.get_session_id() or os.urandom(16).hex()
        sessions = self.get_json(SESSION)
        sessions[session_id] = session
        self.save_data(SESSION, sessions)

        return session_id

    def get_session_id(self):
        cookie = self.headers.get("Cookie")
        print(f"COOOKIEEE = {cookie}")
        if not cookie:
            return {}
        return cookie

    def goodbye_response(self,method,path):
        self.visits_counter(path)
        if hour in range(6, 11):
            msg = f"\n\t\t\t\t   Good morning!"
        elif hour in range(12, 24):
            msg = f"\n\t\t\t\t   Good day!"
        else:
            msg = f"\n\t\t\t\t   Good night!"

        self.respond_200(msg,"text/plain")


    def theme_handler(self,method, path):
        self.visits_counter(path)
        switcher = {
            'get': self.theme_GETresponse,
            'post': self.theme_POSTresponse
        }
        switcher = switcher[method]
        switcher(path)

    def theme_GETresponse(self,path):
        theme = self.get_json(THEME)
        theme_page = self.get_content(THEME_INDEX).format(**theme)
        self.respond_200(theme_page, "text/html")

    def theme_POSTresponse(self, path):
        theme = self.get_json(THEME)
        theme["background_color"], theme["text_color"] = theme["text_color"], theme["background_color"]
        print(theme)
        self.save_data(THEME, theme)
        self.respond_302("/theme",cookie="")

    def counter_response(self,method,path):
        self.visits_counter(path)
        counts = self.get_json(COUNTER)
        file_name = PORTFOLIO / "stats" / "index.html"
        content = self.get_content(file_name).format(**counts)
        self.respond_200(content, "text/html")

    def aboutme_response(self,method,path):
        self.visits_counter(path)
        file_name = PORTFOLIO / "aboutme" / "index.html"
        content = self.get_content(file_name)
        self.respond_200(content, "text/html")

    def education_response(self,method,path):
        self.visits_counter(path)
        edu_info = self.get_json(EDUCATION)
        file_name = PORTFOLIO / "education" / "index.html"
        content = self.get_content(file_name).format(**edu_info)
        self.respond_200(content, "text/html")

    def projects_response(self,method,path):
        self.visits_counter(path)
        file_name = PORTFOLIO / "projects" / "index.html"
        content = self.get_content(file_name)
        self.respond_200(content, "text/html")

    def parse_user_sessions(self) -> Dict[str, str]:
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        payload = data.decode()
        qs = parse_qs(payload)
        user_data = {}
        for key, values in qs.items():
            if not values:
                continue
            user_data[key] = values[0]
        return user_data

    def get_request_payload(self) -> str:
        try:
            content_length = int(self.headers[("content-length")])
            payload = self.rfile.read(content_length)
        except (KeyError, ValueError):
            payload = ""
        print(payload.decode())
        return payload.decode()

    def visits_counter(self, path):
        arguments = self.get_json(COUNTER)
        if path not in arguments:
            arguments[path] = 1
        else:
            arguments[path] = arguments[path] + 1
        print(arguments)
        self.save_data(COUNTER, arguments)

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
        try:
            with file_info.open("r", encoding="utf-8") as usf:
                return json.load(usf)  # what does load?
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def get_content(self, file_name: Path):
        if not file_name.is_file():
            raise NotFound()

        with file_name.open("r") as fp:
            content = fp.read()

        return content

    def get_picture(self, file_name: Path):
        if not file_name.is_file():
            raise NotFound()

        with file_name.open("rb") as picture:
            image = picture.read()

        return image

    def save_data(self, file, arguments: Dict) -> None:
        with file.open("w") as fp:
           json.dump(arguments, fp)


    def respond_200(self, msg, content_type):
        self.response(msg, 200, content_type)

    def respond_302(self, redirect,cookie):
        self.response("", 302, "text/plain", redirect,cookie)

    def respond_404(self,msg, content_type):
        self.response(msg, 404 , content_type)

    def response(self, msg, status_code, content_type="text/plain", redirect="",cookie=""):
        print(cookie)
        self.send_response(status_code)
        self.send_header("Content-type", content_type)
        self.send_header("Content-length", str(len(msg)))
        self.send_header("Location",redirect)
        self.send_header("Set-Cookie", cookie)
        self.end_headers()

        if isinstance(msg, str):
            msg = msg.encode()
        self.wfile.write(msg)

    def linearize_qs(self, qs: Dict) -> Dict:
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


with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("it works")
    httpd.serve_forever()

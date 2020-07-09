import json
import os
import socketserver
import datetime
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from typing import Dict
from urllib.parse import parse_qs

PROJECT_DIR = Path(__file__).parent.parent.resolve()
print(f"PROJECT_DIR = {PROJECT_DIR}")

PORTFOLIO = PROJECT_DIR / "portfolio"
print(f"PORTFOLIO = {PORTFOLIO}")

EDUCATION = PORTFOLIO / "education" / "education.json"

COUNTER = PROJECT_DIR / "data" / "counters.json"

THEME = PROJECT_DIR / "data" / "theme.json"

THEME_INDEX = PORTFOLIO / "theme" / "index.html"

SESSION = PROJECT_DIR / "data" / "session.json"

PROJECTS = PROJECT_DIR / "data" / "projects.json"

PROJECTS_INDEX = PORTFOLIO / "test_projects" / "index.html"
year = datetime.datetime.now().year
hour = datetime.datetime.now().hour

PORT = int(os.getenv("PORT", 8000))
print(f"PORT = {PORT}")


class NotFound(Exception):
    ...


class Missing_Data(Exception):
    ...


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            self.do("get")
        except NotFound:
            file_name = PROJECT_DIR / "images" / "error404.jpg"
            image = self.get_picture(file_name)
            self.respond_404(image, "image/jpeg")

    def do_POST(self):
        try:
            self.do("post")
        except NotFound:
            file_name = PROJECT_DIR / "images" / "error404.jpg"
            image = self.get_picture(file_name)
            self.respond_404(image, "image/jpeg")

    def do(self, method: str):
        default_handler = super().do_GET
        path = self.path_calculating()
        handlers = {
            "/hello": self.handler_hello,
            "/goodbye": self.get_page_goodbye,
            "/aboutme": self.get_portfolio,
            "/projects": self.get_projects,
            "/education": self.get_edu_page,
            "/theme": self.theme_handler,
            "/counter": self.get_stats,
            "": default_handler,
            "/test_projects": self.projects_handler,
            "/test_projects/editing": self.get_editing_page,
            "/test_projects/editing/add": self.projects_handler,
            "/test_projects/editing/delete": self.projects_handler,
            "/test_projects/editing/change": self.projects_handler,
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
        except Missing_Data:
            self.respond_400()

    def handler_hello(self, method: str, path):
        self.visits_counter(path)
        switcher = {"get": self.hello_GETresponse, "post": self.hello_POSTresponse}
        handler = switcher[method]
        handler(path)

    def hello_GETresponse(self, path):
        sessions = self.load_user_session(SESSION) or self.parse_function()
        name = self.name_calculating(sessions)
        age = self.age_calculating(sessions)

        born = None

        if age:
            born = year - age

        html_content = PROJECT_DIR / "hello" / "hello.html"
        hello_page = self.get_content(html_content).format(name=name, year=born)
        self.respond_200(hello_page, "text/html")

    def hello_POSTresponse(self, path):
        form = self.parse_user_sessions()
        session = self.load_user_session(SESSION)
        session.update(form)
        session_id = self.save_user_session(session, SESSION)
        self.respond_302("/hello", session_id)

    def get_page_goodbye(self, method, path):
        self.visits_counter(path)
        if hour in range(6, 11):
            msg = f"\n\t\t\t\t   Good morning!"
        elif hour in range(12, 24):
            msg = f"\n\t\t\t\t   Good day!"
        else:
            msg = f"\n\t\t\t\t   Good night!"

        self.respond_200(msg, "text/plain")

    def theme_handler(self, method, path):
        self.visits_counter(path)
        switcher = {"get": self.theme_GETresponse, "post": self.theme_POSTresponse}
        switcher = switcher[method]
        switcher(path)

    def switch_color(self, theme):
        if not theme:
            theme["background_color"] = "white"
            theme["text_color"] = "black"

        return theme

    def theme_GETresponse(self, path):
        theme_session = self.load_user_session(THEME)
        theme = self.switch_color(theme_session)
        theme_page = self.get_content(THEME_INDEX).format(**theme)
        self.respond_200(theme_page, "text/html")

    def theme_POSTresponse(self, path):
        theme_session = self.load_user_session(THEME)
        theme = self.switch_color(theme_session)
        theme["background_color"], theme["text_color"] = (
            theme["text_color"],
            theme["background_color"],
        )

        session_id = self.save_user_session(theme, THEME)
        self.respond_302("/theme", session_id)

    def projects_handler(self, method, path):
        self.visits_counter(path)

        switcher = {
            "get": self.projects_GETresponse,
            "post": self.projects_editing_handler,
        }
        switcher = switcher[method]

        switcher(path)

    def projects_editing_handler(self, path):
        switcher = {
            "/test_projects/editing/add": self.add_project,
            "/test_projects/editing/delete": self.delete_project,
            "/test_projects/editing/change": self.change_project,
        }

        handler = switcher[path]
        handler()

    def projects_GETresponse(self, method):
        projects_content = self.get_json(PROJECTS)
        projects = ""

        for project in projects_content:
            projects += (
                "<h3>"
                + "PROJECT_NAME:"
                + projects_content[project]["project_name"]
                + "</h3>"
                + "<p>"
                + f"PROJECT_ID: {project}"
                + "</p>"
            )
            projects += (
                "<p>"
                + "PROJECT_DATE:"
                + projects_content[project]["project_date"]
                + "</p>"
            )
            projects += (
                "<p>"
                + "PROJECT_DESCRIPTION:"
                + projects_content[project]["project_description"]
                + "</p>"
            )

        page_content = self.get_content(PROJECTS_INDEX).format(projects=projects)
        self.respond_200(page_content, "text/html")

    def get_editing_page(self, method, path):
        edit_page = self.get_content(PORTFOLIO / "test_projects" / "edit_projects.html")
        self.respond_200(edit_page, "text/html")

    def add_project(self):
        form_content = self.parse_user_sessions()

        if (
            "project_name" not in form_content
            or "project_id" not in form_content
            or "project_description" not in form_content
            or "project_date" not in form_content
        ):
            raise Missing_Data()

        projects = self.get_json(PROJECTS)

        new_project = {}

        id_new_project = form_content["project_id"]

        if id_new_project in projects:
            raise Missing_Data()

        new_project[id_new_project] = {
            "project_name": "",
            "project_description": "",
            "project_date": "",
        }

        for item in form_content:
            if item in new_project[id_new_project]:
                new_project[id_new_project][item] = form_content[item]

        projects.update(new_project)

        self.save_data(PROJECTS, projects)

        self.respond_302("/test_projects", "")

    def delete_project(self):
        form = self.parse_user_sessions()
        projects = self.get_json(PROJECTS)

        if "project_id" not in form:
            raise Missing_Data()

        project_id = form["project_id"]

        if project_id not in projects:
            raise Missing_Data()

        projects.pop(project_id)
        self.save_data(PROJECTS, projects)
        self.respond_302("/test_projects", "")

    def change_project(self):
        form = self.parse_user_sessions()
        projects = self.get_json(PROJECTS)

        if "project_id" not in form:
            raise Missing_Data()

        for item in form:
            if item != "project_id":
                projects[form["project_id"]][item] = form[item]

        self.save_data(PROJECTS, projects)
        self.respond_302("/test_projects", "")

    def get_stats(self, method, path):
        self.visits_counter(path)
        counts = self.get_json(COUNTER)

        today = datetime.date.today()

        stats = {}

        for page in counts:
            stats[page] = {}
            stats[page]["today"] = self.stats_calculating(counts[page],today,0)
            stats[page]["yesterday"] = self.stats_calculating(counts[page],today - datetime.timedelta(days=1),0)
            stats[page]["week"] = self.stats_calculating(counts[page],today,7)
            stats[page]["month"] = self.stats_calculating(counts[page], today, 30)

        html = """<tr>
                   <th>Page</th>
                   <th>Today</th>
                   <th>Yesterday</th> 
                   <th>Week</th>
                   <th>Month</th>
                  </tr>"""
        for page, visits in stats.items():
            html += f"<tr><td>{page}</td>"
            for date, count in visits.items():
                html += f"<td>{count}</td>"
        html += "</tr>"

        file_name = PORTFOLIO / "stats" / "index.html"
        content = self.get_content(file_name).format(stats=html)
        self.respond_200(content, "text/html")


    def stats_calculating(self,page,start_day,days):
        visit_counter = 0

        for day_counter in range(0,days+1):
            day = str(start_day - datetime.timedelta(days=day_counter))
            if day in page:
                visit_counter += page[day]

        return visit_counter


    def get_portfolio(self, method, path):
        self.visits_counter(path)
        file_name = PORTFOLIO / "aboutme" / "index.html"
        content = self.get_content(file_name)
        self.respond_200(content, "text/html")

    def get_edu_page(self, method, path):
        self.visits_counter(path)
        edu_info = self.get_json(EDUCATION)
        file_name = PORTFOLIO / "education" / "index.html"
        content = self.get_content(file_name).format(**edu_info)
        self.respond_200(content, "text/html")

    def get_projects(self, method, path):
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
        return payload.decode()

    def visits_counter(self, path):
        counts = self.get_json(COUNTER)
        today = str(datetime.date.today())

        if path not in counts:
            counts[path] = {}
        if today not in counts[path]:
            counts[path][today] = 0
        counts[path][today] += 1
        self.save_data(COUNTER, counts)

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

    def load_user_session(self, file_name):
        session_id = self.get_session_id()
        if not session_id:
            return {}
        session = self.get_json(file_name)
        return session.get(session_id, {})

    def save_user_session(self, session, file_name):
        session_id = self.get_session_id() or os.urandom(16).hex()
        sessions = self.get_json(file_name)
        sessions[session_id] = session
        self.save_data(file_name, sessions)

        return session_id

    def get_session_id(self):
        cookie = self.headers.get("Cookie")
        if not cookie:
            return {}
        return cookie

    def respond_200(self, msg, content_type):
        self.response(msg, 200, content_type)

    def respond_302(self, redirect, cookie):
        self.response("", 302, "text/plain", redirect, cookie)

    def respond_400(self, msg="You miss something..."):
        self.response(msg, 400, "text/plain")

    def respond_404(self, msg, content_type):
        self.response(msg, 404, content_type)

    def response(
        self, msg, status_code, content_type="text/plain", redirect="", cookie=""
    ):
        print(cookie)
        self.send_response(status_code)
        self.send_header("Content-type", content_type)
        self.send_header("Content-length", str(len(msg)))
        self.send_header("Location", redirect)
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

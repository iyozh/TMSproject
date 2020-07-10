import datetime
import os
import socketserver
from http.server import SimpleHTTPRequestHandler
from pathlib import Path

from src.responses import respond_400, respond_200, respond_302 , respond_404
from src.errors import NotFound, Missing_Data
from src.file_utils import get_picture, get_content
from src.json_utils import get_json, save_data
from src.session_utils import parse_user_sessions, load_user_session, save_user_session
from src.theme_utils import switch_color
from src.utils import parse_function, age_calculating, name_calculating, path_calculating

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

PROJECTS_TEMPLATE = PORTFOLIO / "test_projects" / "projects_template.html"

TABLE_TEMPLATE = PORTFOLIO / "stats" / "table_template.html"

TABLE_PAGES = PORTFOLIO / "stats" / "table_pages.html"

TABLE_COUNTS = PORTFOLIO / "stats" / "table_counts.html"

year = datetime.datetime.now().year
hour = datetime.datetime.now().hour

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
            "/hello": self.handler_hello,
            "/goodbye": self.get_page_goodbye,
            "/aboutme": self.get_portfolio,
            "/projects": self.get_projects,
            "/education": self.edu_handler,
            "/education/night_mode": self.edu_handler,
            "/theme": self.theme_handler,
            "/theme/night_mode": self.theme_handler,
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
            image = get_picture(file_name)
            respond_404(self,image, "image/jpeg")
        except Missing_Data:
            respond_400(self)

    def handler_hello(self, method: str, path):
        self.visits_counter(path)
        switcher = {"get": self.hello_GETresponse, "post": self.hello_POSTresponse}
        handler = switcher[method]
        handler(path)

    def hello_GETresponse(self, path):
        sessions = load_user_session(self, SESSION) or parse_function(self,path)
        name = name_calculating(sessions)
        age = age_calculating(sessions)

        born = None

        if age:
            born = year - age

        html_content = PROJECT_DIR / "hello" / "hello.html"
        hello_page = get_content(html_content).format(name=name, year=born)
        respond_200(self,hello_page, "text/html")

    def hello_POSTresponse(self, path):
        form = parse_user_sessions(self)
        session = load_user_session(self, SESSION)
        session.update(form)
        session_id = save_user_session(self, session, SESSION)
        respond_302(self, "/hello", session_id)

    def get_page_goodbye(self, method, path):
        self.visits_counter(path)
        if hour in range(6, 11):
            msg = f"\n\t\t\t\t   Good morning!"
        elif hour in range(12, 24):
            msg = f"\n\t\t\t\t   Good day!"
        else:
            msg = f"\n\t\t\t\t   Good night!"

        respond_200(self, msg, "text/plain")

    def theme_handler(self, method, path):
        switcher = {"get": self.get_theme_page, "post": self.post_theme_page}
        handler = switcher[method]
        handler(path,"/theme")

    def post_theme_page(self,path, endpoint):
        switcher = {
            "/theme/night_mode": self.change_mode
        }
        handler = switcher[path]

        handler(path, endpoint)

    def get_theme_page(self, path,redirect):
        self.visits_counter(path)
        theme_session = load_user_session(self, THEME)
        theme = switch_color(theme_session)
        theme_page = get_content(THEME_INDEX).format(**theme)
        respond_200(self,theme_page, "text/html")

    def projects_handler(self, method, path):

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

    def projects_GETresponse(self,path):
        self.visits_counter(path)
        projects_content = get_json(PROJECTS)
        template = get_content(PROJECTS_TEMPLATE)
        projects = ""

        for project in projects_content:
            projects += template.format(
                project_name=projects_content[project]["project_name"],
                project_id=project,
                project_date=projects_content[project]["project_date"],
                project_description=projects_content[project]["project_description"],
            )

        page_content = get_content(PROJECTS_INDEX).format(projects=projects)
        respond_200(self, page_content, "text/html")

    def get_editing_page(self, method, path):
        self.visits_counter(path)
        edit_page = get_content(PORTFOLIO / "test_projects" / "edit_projects.html")
        respond_200(self, edit_page, "text/html")

    def add_project(self):
        form_content = parse_user_sessions(self)

        if (
                "project_name" not in form_content
                or "project_id" not in form_content
                or "project_description" not in form_content
                or "project_date" not in form_content
        ):
            raise Missing_Data()

        projects = get_json(PROJECTS)

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

        save_data(PROJECTS, projects)

        respond_302(self, "/test_projects", "")

    def delete_project(self):
        form = parse_user_sessions(self)
        projects = get_json(PROJECTS)

        if "project_id" not in form:
            raise Missing_Data()

        project_id = form["project_id"]

        if project_id not in projects:
            raise Missing_Data()

        projects.pop(project_id)
        save_data(PROJECTS, projects)
        respond_302(self, "/test_projects", "")

    def change_project(self):
        form = parse_user_sessions(self)
        projects = get_json(PROJECTS)

        if "project_id" not in form:
            raise Missing_Data()

        for item in form:
            if item != "project_id":
                projects[form["project_id"]][item] = form[item]

        save_data(PROJECTS, projects)
        respond_302(self,"/test_projects", "")

    def get_stats(self, method, path):
        self.visits_counter(path)
        counts = get_json(COUNTER)

        today = datetime.date.today()

        stats = {}

        for page in counts:
            stats[page] = {}
            stats[page]["today"] = self.stats_calculating(counts[page], today, 0)
            stats[page]["yesterday"] = self.stats_calculating(
                counts[page], today - datetime.timedelta(days=1), 0
            )
            stats[page]["week"] = self.stats_calculating(counts[page], today, 7)
            stats[page]["month"] = self.stats_calculating(counts[page], today, 30)

        table_template = get_content(TABLE_TEMPLATE)
        for page, visits in stats.items():
            table_template += get_content(TABLE_PAGES).format(page=page)
            for date, count in visits.items():
                table_template += get_content(TABLE_COUNTS).format(count=count)

        file_name = PORTFOLIO / "stats" / "index.html"
        content = get_content(file_name).format(stats=table_template)
        respond_200(self,content, "text/html")

    def stats_calculating(self, page, start_day, days):
        visit_counter = 0

        for day_counter in range(0, days + 1):
            day = str(start_day - datetime.timedelta(days=day_counter))
            if day in page:
                visit_counter += page[day]

        return visit_counter

    def get_portfolio(self, method, path):
        self.visits_counter(path)
        file_name = PORTFOLIO / "aboutme" / "index.html"
        content = get_content(file_name)
        respond_200(self, content, "text/html")

    def edu_handler(self,method,path):

        switcher = {
            "get": self.get_edu_page,
            "post": self.post_edu_page,
        }
        handler = switcher[method]

        handler(path,"/education")

    def post_edu_page(self,path,endpoint):
        switcher = {
            "/education/night_mode": self.change_mode
        }
        handler = switcher[path]

        handler(path,endpoint)

    def change_mode(self, path,redirect):
        theme_session = load_user_session(self,THEME)
        theme = switch_color(theme_session)
        theme["background_color"], theme["text_color"] = (
            theme["text_color"],
            theme["background_color"],
        )

        session_id = save_user_session(self, theme, THEME)
        respond_302(self,redirect, session_id)


    def get_edu_page(self, path,redirect):
        self.visits_counter(path)
        theme_session = load_user_session(self, THEME)
        theme = switch_color(theme_session)
        edu_info = get_json(EDUCATION)
        file_name = PORTFOLIO / "education" / "index.html"
        content = get_content(file_name).format(**edu_info, **theme)
        respond_200(self,content, "text/html")

    def get_projects(self, method, path):
        self.visits_counter(path)
        file_name = PORTFOLIO / "projects" / "index.html"
        content = get_content(file_name)
        respond_200(self,content, "text/html")

    def visits_counter(self, path):
        counts = get_json(COUNTER)
        today = str(datetime.date.today())

        if path not in counts:
            counts[path] = {}
        if today not in counts[path]:
            counts[path][today] = 0
        counts[path][today] += 1
        save_data(COUNTER, counts)






with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("it works")
    httpd.serve_forever()

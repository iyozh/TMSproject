from django.conf import settings

PORTFOLIO = settings.REPO_DIR / "portfolio"


EDUCATION = PORTFOLIO / "education" / "education.json"

COUNTER = settings.REPO_DIR / "data" / "counters.json"

THEME = settings.REPO_DIR / "data" / "theme.json"

THEME_INDEX = PORTFOLIO / "theme" / "index.html"

SESSION = settings.REPO_DIR / "data" / "session.json"

PROJECTS = settings.REPO_DIR / "data" / "projects.json"

PROJECTS_INDEX = PORTFOLIO / "test_projects" / "index.html"

PROJECTS_TEMPLATE = PORTFOLIO / "test_projects" / "projects_template.html"

TABLE_TEMPLATE = PORTFOLIO / "stats" / "table_template.html"

TABLE_PAGES = PORTFOLIO / "stats" / "table_pages.html"

TABLE_COUNTS = PORTFOLIO / "stats" / "table_counts.html"

RESUME_CSS = PORTFOLIO / "aboutme" / "css" / "main.css"

PROJECTS_CSS = PORTFOLIO / "projects" / "css" / "main.css"

RESUME_INDEX = PORTFOLIO / "aboutme" / "index.html"

HELLO_PAGE = settings.REPO_DIR / "hello" / "hello.html"

MY_PROJECTS_PAGE = PORTFOLIO / "projects" / "index.html"
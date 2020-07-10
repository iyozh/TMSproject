from pathlib import Path

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

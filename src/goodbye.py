import datetime

from src.responses import respond_200
from src.stats import visits_counter

hour = datetime.datetime.now().hour


def get_page_goodbye(self, method, path):
    visits_counter(path)
    if hour in range(6, 11):
        msg = f"\n\t\t\t\t   Good morning!"
    elif hour in range(12, 24):
        msg = f"\n\t\t\t\t   Good day!"
    else:
        msg = f"\n\t\t\t\t   Good night!"

    respond_200(self, msg, "text/plain")

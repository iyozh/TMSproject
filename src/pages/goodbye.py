import datetime

from django.http import HttpResponse


def get_page_goodbye(request):
    hour = datetime.datetime.now().hour

    if hour in range(6, 11):
        msg = f"\n\t\t\t\t   Good morning!"
    elif hour in range(12, 24):
        msg = f"\n\t\t\t\t   Good day!"
    else:
        msg = f"\n\t\t\t\t   Good night!"

    return HttpResponse(msg)

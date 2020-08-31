from django.contrib.sessions.models import Session
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Truncate sessions"

    def handle(self, *args, **options):
        Session.objects.all().delete()

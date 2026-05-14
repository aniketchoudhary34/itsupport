from django.core.management.base import BaseCommand

from myapp.email_reader import fetch_tickets_from_email


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        fetch_tickets_from_email()

        self.stdout.write("Emails checked successfully")
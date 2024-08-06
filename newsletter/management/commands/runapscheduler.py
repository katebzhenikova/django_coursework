from django.core.management import BaseCommand

from newsletter.services import send_newsletter_periodic


class Command(BaseCommand):
    """Команда на запуск рассылки"""

    def handle(self, *args, **options):

        send_newsletter_periodic()


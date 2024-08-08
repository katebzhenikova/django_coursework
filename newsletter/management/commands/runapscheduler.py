from django.core.management import BaseCommand

from newsletter.services import send_newsletter_periodic, start_scheduler


class Command(BaseCommand):
    help = 'Запуск планировщика для рассылок'

    def handle(self, *args, **options):
        start_scheduler()
        self.stdout.write(self.style.SUCCESS('Планировщик успешно запущен'))



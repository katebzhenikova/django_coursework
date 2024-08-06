import os

from django.apps import AppConfig


class NewsletterConfig(AppConfig):
    name = 'newsletter'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'True':
            from newsletter.services import start_scheduler
            start_scheduler()

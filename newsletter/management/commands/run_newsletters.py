from datetime import timezone, datetime, timedelta

from django.core.management.base import BaseCommand
from django_apscheduler.models import DjangoJobExecution, DjangoJob
from apscheduler.schedulers.background import BackgroundScheduler

from newsletter.models import NewsletterMessage, NewsletterLog, NewsletterSettings
from newsletter.send_newsletter import send_newsletter


class Command(BaseCommand):
    def handle(self, *args, **options):
        send_newsletter()

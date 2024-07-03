import logging
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from newsletter.services import send_letter
from newsletter.models import NewsletterSettings
from datetime import datetime
from pytz import utc

logger = logging.getLogger(__name__)


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler(timezone=utc)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Удаление старых выполнений задач
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),  # каждый понедельник в 00.00
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        # Добавление задач рассылки
        for ns in NewsletterSettings.objects.filter(is_active=True):
            # Переводим время в UTC
            scheduled_time = ns.time
            # Создаем триггер в зависимости от периодичности
            if ns.frequency == 'daily':
                trigger = CronTrigger(hour=scheduled_time.hour, minute=scheduled_time.minute)
            elif ns.frequency == 'weekly':
                trigger = CronTrigger(day_of_week=ns.start_at.weekday(), hour=scheduled_time.hour,
                                      minute=scheduled_time.minute)
            elif ns.frequency == 'monthly':
                trigger = CronTrigger(day=ns.start_at.day, hour=scheduled_time.hour, minute=scheduled_time.minute)

            scheduler.add_job(
                send_letter,
                trigger=trigger,
                id=f"send_letter_{ns.id}",  # Уникальный ID для каждой задачи
                max_instances=1,
                replace_existing=True,
                kwargs={'newsletter_settings_id': ns.id}  # Передаем ID настроек рассылки в функцию
            )
            logger.info(f"Added job for NewsletterSettings id={ns.id}.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

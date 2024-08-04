from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from newsletter.services import send_letter
from newsletter.models import NewsletterSettings
from datetime import datetime, timedelta
from pytz import utc
import logging

logger = logging.getLogger(__name__)

@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    logger.info("Deleting old job executions...")
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

def send_letter_wrapper(newsletter_settings_id):
    logger.info(f"Sending letter for NewsletterSettings id={newsletter_settings_id}...")
    try:
        send_letter(newsletter_settings_id)
        logger.info(f"Letter sent successfully for NewsletterSettings id={newsletter_settings_id}.")
    except Exception as e:
        logger.error(f"Error sending letter for NewsletterSettings id={newsletter_settings_id}: {e}")


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        global next_run_time
        scheduler = BackgroundScheduler(timezone=utc)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Удаление старых выполнений задач
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),  # каждый понедельник в 00:00
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        # Добавление задач рассылки
        for ns in NewsletterSettings.objects.filter(is_active=True):
            scheduled_time = ns.time
            current_time = datetime.now(tz=utc)

            # Определяем следующую дату отправки в зависимости от периодичности
            if ns.frequency == 'daily':
                next_run_time = current_time + timedelta(days=1)
            elif ns.frequency == 'weekly':
                next_run_time = current_time + timedelta(weeks=1)
            elif ns.frequency == 'monthly':
                next_run_time = current_time + timedelta(days=30)

            # Устанавливаем конкретное время отправки
            next_run_time = next_run_time.replace(hour=scheduled_time.hour, minute=scheduled_time.minute, second=0, microsecond=0)

            # Проверяем, если следующая дата отправки уже прошла, сдвигаем её на следующий период
            if next_run_time <= current_time:
                if ns.frequency == 'daily':
                    next_run_time += timedelta(days=1)
                elif ns.frequency == 'weekly':
                    next_run_time += timedelta(weeks=1)
                elif ns.frequency == 'monthly':
                    next_run_time += timedelta(days=30)

            # Добавляем задачу в расписание
            scheduler.add_job(
                send_letter,
                trigger=DateTrigger(run_date=next_run_time),
                id=f"send_letter_{ns.id}",  # Уникальный ID для каждой задачи
                max_instances=1,
                replace_existing=True,
                kwargs={'newsletter_settings_id': ns.id}  # Передаем ID настроек рассылки в функцию
            )
            logger.info(f"Added job for NewsletterSettings id={ns.id} at {next_run_time}.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

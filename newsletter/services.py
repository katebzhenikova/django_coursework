import smtplib
from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.core.mail import send_mail

from newsletter.models import NewsletterSettings, NewsletterMessage, NewsletterLog
from apscheduler.schedulers.background import BackgroundScheduler


def send_newsletter_email(objects):
    try:
        message_instance = NewsletterMessage.objects.first()
        server_response = send_mail(
            subject=message_instance.newsletter_topic,
            message=message_instance.newsletter_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client.client_email for client in objects.clients.all()],
            fail_silently=False,
        )
        log = NewsletterLog.objects.create(sending=objects, server_response=server_response)
        if server_response:
            log.status = True
            log.save()
        if objects.status == 'Создана':
            objects.status = 'Запущена'
            objects.save()
    except smtplib.SMTPException as e:
        log = NewsletterLog.objects.create(sending=objects, server_response=e)
        log.save()


def send_newsletter_periodic():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    print(f'Текущее время - {current_datetime}')

    for obj in NewsletterSettings.objects.all():
        if obj.start_at < current_datetime < obj.finish_at:
            log = NewsletterLog.objects.filter(sending=obj)
            print(log)
            if log.exists():
                last_log = log.order_by('last_tried_at').last()
                current_timedelta = current_datetime - last_log.last_tried_at
                print(obj.frequency)

                if obj.frequency == 'daily' and current_timedelta >= timedelta(days=1):
                    send_newsletter_email(obj)
                    print(f'Рассылка раз в день выполнена успешно')
                elif obj.frequency == 'weekly' and current_timedelta >= timedelta(weeks=1):
                    send_newsletter_email(obj)
                    print(f'Рассылка раз в неделю выполнена успешно')
                elif obj.frequency == 'monthly' and current_timedelta >= timedelta(
                        weeks=4):
                    send_newsletter_email(obj)
                    print(f'Рассылка раз в месяц выполнена успешно')

            else:
                send_newsletter_email(obj)
        elif current_datetime > obj.finish_at:
            obj.status = 'Завершена'
            obj.save()


def start_scheduler():
    """Проверка добавлена ли задача"""
    scheduler = BackgroundScheduler()

    if not scheduler.get_jobs():
        scheduler.add_job(send_newsletter_periodic, 'interval', minutes=1)

    if not scheduler.running:
        scheduler.start()

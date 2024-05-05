# from datetime import timezone
#
# from django_apscheduler.models import DjangoJobExecution
# from django.core.mail import send_mail
#
# from newsletter.models import NewsletterLog, NewsletterMessage, NewsletterSettings
#
#
# def send_newsletter():
#     # Получить все активные рассылки
#     newsletters = NewsletterSettings.objects.filter(status='running')
#
#     # Для каждой рассылки
#     for newsletter in newsletters:
#         # Получить список клиентов
#         subscribers = newsletter.clients.all()
#
#         # Для каждого подписчика
#         for subscriber in subscribers:
#             # Отправить письмо
#             send_mail(
#                 newsletter.message.subject,
#                 newsletter.message.body,
#                 'katomyr@mail.ru',
#                 [subscriber.email],
#                 fail_silently=False,
#             )
#
#         # Обновить статус рассылки
#         newsletter.status = 'completed'
#         newsletter.save()
#
#         # Записать лог рассылки
#         NewsletterLog.objects.create(
#             date_time=timezone.now(),
#             status='success',
#             response='Письмо успешно отправлено всем клиентам.'
#         )

import smtplib
from django.core.mail import send_mail
from django.conf import settings
from newsletter.models import NewsletterLog, NewsletterMessage, NewsletterSettings
from datetime import datetime, timedelta
import pytz


def my_scheduled_job():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    sendings = NewsletterSettings.objects.all().filter(status='создана').filter(is_active=True).filter(start_at__lte=current_datetime).filter(finish_at__gte=current_datetime)
    print(sendings)
    print(current_datetime)
    for sending in sendings:
        sending.status = 'executing'
        sending.save()
        email_list = [client.email for client in sending.clients.all()]

        try:
            server_response = send_mail(
                subject=sending.message.theme,
                message=sending.message.text,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=email_list,
                fail_silently=False,
            )

            newsletterlog = NewsletterLog(sending=sending, status=True, server_response=server_response)
            newsletterlog.save()

            if not sending.sent_at:
                sending.sent_at = current_datetime

        except smtplib.SMTPException as e:
            newsletterlog = NewsletterLog(sending=sending, status=False, server_response=e)
            newsletterlog.save()

        finally:
            if sending.period == 'раз в день':
                sending.start_at = newsletterlog.last_tried_at + timedelta(days=1)
            elif sending.period == 'раз в неделю':
                sending.start_at = newsletterlog.last_tried_at + timedelta(weeks=1)
            elif sending.period == 'раз в месяц':
                sending.start_at = newsletterlog.last_tried_at + timedelta(days=30)

            if sending.start_at < sending.finish_at:
                sending.status = 'created'
            else:
                sending.status = 'finished'
                sending.is_active = False
            sending.save()


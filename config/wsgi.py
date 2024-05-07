from datetime import timezone, datetime
from newsletter.models import NewsletterSettings

from django_apscheduler.models import DjangoJobExecution
from django.core.mail import send_mail

from newsletter.models import NewsletterLog, NewsletterMessage, NewsletterSettings

import os
from django.core.wsgi import get_wsgi_application
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

scheduler = BackgroundScheduler()
scheduler.configure(jobstores={'default': DjangoJobStore()})
scheduler.start()


def run_newsletter():
    newsletters = NewsletterSettings.objects.filter(status='running')

    # Для каждой рассылки
    for newsletter in newsletters:
        # Получить список клиентов
        subscribers = newsletter.clients.all()

        # Для каждого подписчика
        for subscriber in subscribers:
            # Отправить письмо
            send_mail(
                newsletter.message.newsletter_topic,
                newsletter.message.newsletter_message,
                'katomyr@mail.ru',
                [subscriber.client_email],
                fail_silently=False,
            )

        # Обновить статус рассылки
        newsletter.status = 'completed'
        newsletter.save()

        # Записать лог рассылки
        NewsletterLog.objects.create(
            last_tried_at=datetime.now(),
            status='success',
            server_response='Письмо успешно отправлено всем клиентам.'
        )


# Функция для добавления задачи рассылки в планировщик
def schedule_newsletter(frequency, newsletter_id):
    # Определение интервала
    interval = {'daily': 1, 'weekly': 7, 'monthly': 30}.get(frequency, 1)

    # Добавление задачи в планировщик
    scheduler.add_job(
        run_newsletter,
        'interval',
        days=interval,
        id=str(newsletter_id),  # Уникальный идентификатор задачи
        replace_existing=True,  # Заменить существующую задачу, если она уже есть
        kwargs={'newsletter_id': newsletter_id}
    )


# Запуск планировщика
scheduler.start()


for newsletter in NewsletterSettings.objects.all():
    schedule_newsletter(newsletter.frequency, newsletter.id)


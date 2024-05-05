from datetime import timezone, datetime

from django_apscheduler.models import DjangoJobExecution
from django.core.mail import send_mail

from newsletter.models import NewsletterLog, NewsletterMessage, NewsletterSettings


def send_newsletter():
    # Получить все активные рассылки
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
            date_time=datetime.now(),
            status='success',
            response='Письмо успешно отправлено всем клиентам.'
        )


from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from config.settings import EMAIL_HOST_USER
import django
django.setup()

from newsletter.models import NewsletterSettings, NewsletterLog, NewsletterMessage, Client



def send_letter():
    """Функция отправки сообщения списку клиентов"""
    day = timedelta(days=1)
    week = timedelta(weeks=1)
    month = timedelta(days=30)

    running_newsletters = NewsletterSettings.objects.filter(status='running', is_active=True)

    for newsletter in running_newsletters:
        newsletter_list = [client.client_email for client in newsletter.clients.all()]

        try:
            result = send_mail(
                subject=newsletter.message.newsletter_topic,
                message=newsletter.message.newsletter_message,
                from_email=EMAIL_HOST_USER,
                recipient_list=newsletter_list,
                fail_silently=False,
            )

            status = True if result > 0 else False
            server_response = 'Ошибка почтового сервера' if not status else 'Успешно'

            log = NewsletterLog(
                sending=newsletter,
                status=status,
                last_tried_at=timezone.now(),
                server_response=server_response,
            )
            log.save()

        except Exception as e:
            log = NewsletterLog(
                sending=newsletter,
                status=False,
                last_tried_at=timezone.now(),
                server_response=str(e),
            )
            log.save()


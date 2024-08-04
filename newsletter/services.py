from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from config.settings import EMAIL_HOST_USER
from newsletter.models import NewsletterSettings, NewsletterLog, Client
import logging

logger = logging.getLogger(__name__)


def send_letter(newsletter_settings_id):
    """Функция отправки сообщения списку клиентов"""
    day = timedelta(days=1)
    week = timedelta(weeks=1)
    month = timedelta(days=30)

    # Получаем настройки рассылки по ID
    try:
        newsletter = NewsletterSettings.objects.get(id=newsletter_settings_id)
    except NewsletterSettings.DoesNotExist:
        logger.error(f"NewsletterSettings with id {newsletter_settings_id} does not exist.")
        return

    now = timezone.now()
    newsletter_list = [client.client_email for client in newsletter.clients.all()]

    # Проверяем, соответствует ли текущее время времени отправки
    if newsletter.time <= now.time() and (newsletter.start_at <= now <= newsletter.finish_at):
        # Проверяем периодичность
        if newsletter.frequency == 'daily' or \
                (newsletter.frequency == 'weekly' and now >= newsletter.start_at + week) or \
                (newsletter.frequency == 'monthly' and now >= newsletter.start_at + month):

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
                logger.error(f"Error sending email: {e}", exc_info=True)
                log = NewsletterLog(
                    sending=newsletter,
                    status=False,
                    last_tried_at=timezone.now(),
                    server_response=str(e),
                )
                log.save()
        else:
            logger.info(f"Newsletter id {newsletter_settings_id} is not due for sending yet.")
    else:
        logger.info(f"Newsletter id {newsletter_settings_id} is outside the scheduled time range.")

from django.conf import settings

from django.db import models
from django.utils import timezone
import pytz
from datetime import datetime, timedelta

from config import settings

NULLABLE = {'null': True, 'blank': True}



class Client(models.Model):
    client_email = models.EmailField(unique=True, verbose_name='почта клиента')
    client_fullname = models.CharField(max_length=50, verbose_name='ФИО клиента')
    comment = models.CharField(blank=True, verbose_name='комментарий')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='автор')

    def __str__(self):
        return f'{self.client_fullname}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class NewsletterMessage(models.Model):
    newsletter_topic = models.CharField(max_length=500, verbose_name='тема рассылки')
    newsletter_message = models.TextField(max_length=30, verbose_name='сообщение рассылки')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='автор')

    def __str__(self):
        return f'{self.newsletter_topic}'

    class Meta:
        verbose_name = 'Тема рассылки'


class NewsletterSettings(models.Model):
    time = models.TimeField(verbose_name='Выбрать время')
    frequency = models.CharField(max_length=255, choices=[('daily', 'Раз в день'), ('weekly', 'Раз в неделю'),
                                                          ('monthly', 'Раз в месяц')], verbose_name='Периодичность')
    status = models.CharField(max_length=255,
                              choices=[('completed', 'Завершена'), ('created', 'Создана'), ('running', 'Запущена')],
                              verbose_name='Статус')
    message = models.ForeignKey("NewsletterMessage", on_delete=models.CASCADE, verbose_name='сообщение', **NULLABLE)
    clients = models.ManyToManyField('Client', verbose_name='Клиент')  # Связь "многие ко многим" с моделью клиента
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='автор')

    start_at = models.DateTimeField(default=datetime.now(), verbose_name='дата начала')
    finish_at = models.DateTimeField(default=timezone.now() + timedelta(days=30), verbose_name='дата окончания')
    is_active = models.BooleanField(default=True, verbose_name='активна')

    def __str__(self):
        return f'{self.message}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

        permissions = [
            (
                'set_status',
                'Can change status'
            )
        ]


class NewsletterLog(models.Model):
    sending = models.ForeignKey("NewsletterSettings", on_delete=models.CASCADE, verbose_name='рассылка')
    last_tried_at = models.DateTimeField(default=timezone.now, verbose_name='последняя попытка')
    status = models.BooleanField(default=False, verbose_name='статус')
    server_response = models.CharField(verbose_name='ответ почтового сервера', **NULLABLE)

    def __str__(self):
        str = f'{self.sending} {self.last_tried_at} '
        if self.status:
            str += 'успешная попытка отправки'
        else:
            str += f'ошибка: {self.server_response}'
        return str

    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'
        ordering = ('last_tried_at',)

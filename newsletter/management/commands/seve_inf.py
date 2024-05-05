
from django.core.management import BaseCommand
import json
from django.db import connection

from newsletter.models import Client, NewsletterMessage, NewsletterSettings
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):

        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE main_message RESTART IDENTITY CASCADE;')
            cursor.execute('TRUNCATE TABLE main_sending RESTART IDENTITY CASCADE;')
            cursor.execute('TRUNCATE TABLE main_client RESTART IDENTITY CASCADE;')

        Client.objects.all().delete()
        NewsletterMessage.objects.all().delete()
        NewsletterSettings.objects.all().delete()

        with open('data.json', 'r') as f:
            data = json.load(f)

        clients_to_create = []
        messages_to_create = []

        for item in data:
            if item["model"] == "newsletter.client":
                name, email, owner = item['fields']['name'], item['fields']['email'], item['fields']['owner']
                clients_to_create.append(Client(name=name, email=email, owner=User.objects.get(pk=owner)))
            elif item["model"] == "newsletter.message":
                theme, text, owner = item['fields']['theme'], item['fields']['text'], item['fields']['owner']
                messages_to_create.append(NewsletterMessage(theme=theme, text=text, owner=User.objects.get(pk=owner)))

        Client.objects.bulk_create(clients_to_create)
        NewsletterMessage.objects.bulk_create(messages_to_create)

        for item in data:
            if item["model"] == "newsletter.newslettersettings":
                message = NewsletterMessage.objects.get(pk=item['fields']['message'])
                owner = User.objects.get(pk=item['fields']['owner'])
                s = NewsletterSettings(message=message, owner=owner)
                s.save()
                s.clients.set(item['fields']['clients'])
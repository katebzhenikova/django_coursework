from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    """Создаем суперюзера и командой python manage.py auth записываем данные в БД"""

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@gmail.com',
            first_name='Admin',
            last_name='Coursework',
            is_staff=True,
            is_superuser=True,
        )

        user.set_password('123coursework321')
        user.save()



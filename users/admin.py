"""нужно чтобы в админке http://127.0.0.1:8000/admin/ появились пользователи"""

from django.contrib import admin

from users.models import User

admin.site.register(User)



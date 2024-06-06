from django.contrib import admin

from newsletter.models import Client, NewsletterLog, NewsletterMessage, NewsletterSettings

admin.site.register(Client)
admin.site.register(NewsletterLog)
admin.site.register(NewsletterMessage)
admin.site.register(NewsletterSettings)

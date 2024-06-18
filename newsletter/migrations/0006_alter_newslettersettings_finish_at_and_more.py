# Generated by Django 5.0.3 on 2024-05-21 11:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0005_alter_newslettersettings_finish_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newslettersettings',
            name='finish_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 20, 11, 32, 20, 459893, tzinfo=datetime.timezone.utc), verbose_name='дата окончания'),
        ),
        migrations.AlterField(
            model_name='newslettersettings',
            name='start_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 21, 14, 32, 20, 459893), verbose_name='дата начала'),
        ),
    ]
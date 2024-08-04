# Generated by Django 5.0.3 on 2024-08-04 14:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0017_alter_newslettersettings_finish_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newslettersettings',
            name='finish_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 4, 14, 58, 20, 322193, tzinfo=datetime.timezone.utc), verbose_name='дата окончания'),
        ),
        migrations.AlterField(
            model_name='newslettersettings',
            name='start_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 4, 17, 58, 20, 322193), verbose_name='дата начала'),
        ),
    ]
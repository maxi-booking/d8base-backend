# Generated by Django 2.2.11 on 2020-04-06 06:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20200331_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlocation',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_locations', to=settings.CITIES_COUNTRY_MODEL, verbose_name='country'),
        ),
    ]

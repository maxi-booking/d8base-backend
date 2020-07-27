# Generated by Django 3.0.7 on 2020-07-06 13:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='description',
            field=models.TextField(blank=True, db_index=True, null=True, validators=[django.core.validators.MinLengthValidator(20)], verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_type',
            field=models.CharField(choices=[('online', 'online'), ('professional', "at the professional's location"), ('client', "at the client's location")], max_length=20, verbose_name='account type'),
        ),
    ]
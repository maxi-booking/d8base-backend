# Generated by Django 3.0.7 on 2020-07-10 16:52

from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0035_usersettings_is_last_name_hidden'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersettings',
            name='currency',
            field=djmoney.models.fields.CurrencyField(blank=True, choices=[('CAD', 'Canadian Dollar'), ('EUR', 'Euro'), ('RUB', 'Russian Ruble'), ('USD', 'US Dollar')], default='USD', max_length=3, null=True, verbose_name='currency'),
        ),
    ]

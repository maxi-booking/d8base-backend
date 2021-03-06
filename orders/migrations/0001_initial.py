# Generated by Django 3.0.10 on 2020-11-13 11:53

import d8b.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import djmoney.models.fields
import djmoney.models.validators
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0011_auto_20201028_1023'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('start_datetime', models.DateTimeField(db_index=True, validators=[d8b.validators.validate_datetime_in_future], verbose_name='start datetime')),
                ('end_datetime', models.DateTimeField(db_index=True, validators=[d8b.validators.validate_datetime_in_future], verbose_name='end datetime')),
                ('status', models.CharField(choices=[('not_confirmed', 'not confirmed'), ('confirmed', 'confirmed'), ('paid', 'paid'), ('complete', 'complete'), ('canceled', 'canceled')], default='not_confirmed', max_length=20, verbose_name='status')),
                ('note', models.CharField(blank=True, max_length=255, null=True, verbose_name='note')),
                ('price_currency', djmoney.models.fields.CurrencyField(choices=[('CAD', 'Canadian Dollar'), ('EUR', 'Euro'), ('RUB', 'Russian Ruble'), ('USD', 'US Dollar')], default='USD', editable=False, max_length=3)),
                ('price', djmoney.models.fields.MoneyField(blank=True, db_index=True, decimal_places=4, max_digits=19, null=True, validators=[djmoney.models.validators.MinMoneyValidator(0)], verbose_name='price')),
                ('remind_before', models.PositiveIntegerField(blank=True, db_index=True, help_text='number of minutes for a reminder before the event', null=True, verbose_name='remind')),
                ('is_another_person', models.BooleanField(db_index=True, default=True, verbose_name='Order for another person?')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(max_length=150, verbose_name='last name')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, db_index=True, max_length=128, null=True, region=None, verbose_name='phone')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='user')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders_order_created_by', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders_order_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='modified by')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='services.Service', verbose_name='service')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['-modified', '-created'], name='orders_orde_modifie_646f2e_idx'),
        ),
    ]

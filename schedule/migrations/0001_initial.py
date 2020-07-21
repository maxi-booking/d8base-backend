# Generated by Django 3.0.7 on 2020-07-21 10:53

import d8b.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('services', '0009_auto_20200714_2014'),
        ('professionals', '0019_auto_20200713_1849'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('day_of_week', d8b.fields.DayOfWeekField(choices=[(0, 'monday'), (1, 'tuesday'), (2, 'wednesday'), (3, 'thursday'), (4, 'friday'), (5, 'saturday'), (6, 'sunday')], db_index=True, verbose_name='service')),
                ('start_time', models.TimeField(db_index=True, default=datetime.time(9, 0), verbose_name='start time')),
                ('end_time', models.TimeField(db_index=True, default=datetime.time(18, 0), verbose_name='end time')),
                ('is_enabled', models.BooleanField(db_index=True, default=True, verbose_name='is enabled?')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schedule_serviceschedule_created_by', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schedule_serviceschedule_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='modified by')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule', to='services.Service', verbose_name='service')),
            ],
            options={
                'ordering': ('day_of_week', 'start_time'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProfessionalSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('day_of_week', d8b.fields.DayOfWeekField(choices=[(0, 'monday'), (1, 'tuesday'), (2, 'wednesday'), (3, 'thursday'), (4, 'friday'), (5, 'saturday'), (6, 'sunday')], db_index=True, verbose_name='service')),
                ('start_time', models.TimeField(db_index=True, default=datetime.time(9, 0), verbose_name='start time')),
                ('end_time', models.TimeField(db_index=True, default=datetime.time(18, 0), verbose_name='end time')),
                ('is_enabled', models.BooleanField(db_index=True, default=True, verbose_name='is enabled?')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schedule_professionalschedule_created_by', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schedule_professionalschedule_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='modified by')),
                ('professional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule', to='professionals.Professional', verbose_name='professional')),
            ],
            options={
                'ordering': ('day_of_week', 'start_time'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]

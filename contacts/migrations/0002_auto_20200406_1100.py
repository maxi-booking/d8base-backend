# Generated by Django 2.2.11 on 2020-04-06 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ('name',)},
        ),
    ]
# Generated by Django 2.2.11 on 2020-04-06 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_auto_20200406_1100'),
        ('users', '0012_usercontact'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='usercontact',
            unique_together={('value', 'user', 'contact')},
        ),
    ]

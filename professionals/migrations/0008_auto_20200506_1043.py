# Generated by Django 3.0.5 on 2020-05-06 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0030_auto_20200506_0830'),
        ('professionals', '0007_professionalcontact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='professionalcontact',
            name='use_value_from_user',
        ),
        migrations.AddField(
            model_name='professionalcontact',
            name='use_user_contact',
            field=models.ForeignKey(blank=True, help_text='use contact from the user', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='professional_contacts', to='users.UserContact', verbose_name='user user contact'),
        ),
    ]

# Generated by Django 3.0.10 on 2020-10-28 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_auto_20200904_1138'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='professionalclosedperiod',
            index=models.Index(fields=['-modified', '-created'], name='schedule_pr_modifie_475f62_idx'),
        ),
        migrations.AddIndex(
            model_name='professionalschedule',
            index=models.Index(fields=['-modified', '-created'], name='schedule_pr_modifie_b4edca_idx'),
        ),
        migrations.AddIndex(
            model_name='serviceclosedperiod',
            index=models.Index(fields=['-modified', '-created'], name='schedule_se_modifie_9a9f5f_idx'),
        ),
        migrations.AddIndex(
            model_name='serviceschedule',
            index=models.Index(fields=['-modified', '-created'], name='schedule_se_modifie_489b7a_idx'),
        ),
    ]
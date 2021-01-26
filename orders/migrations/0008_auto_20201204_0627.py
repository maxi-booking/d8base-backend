# Generated by Django 3.0.10 on 2020-12-04 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20201120_1337'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderreminder',
            options={'get_latest_by': 'modified', 'ordering': ('-modified', '-created')},
        ),
        migrations.AlterField(
            model_name='order',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='last name'),
        ),
        migrations.AddIndex(
            model_name='orderreminder',
            index=models.Index(fields=['-modified', '-created'], name='orders_orde_modifie_055023_idx'),
        ),
    ]
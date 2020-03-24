# Generated by Django 2.2.11 on 2020-03-24 07:44

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20200319_1542'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userlocation',
            options={'ordering': ('-created',)},
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='avatars'),
        ),
    ]

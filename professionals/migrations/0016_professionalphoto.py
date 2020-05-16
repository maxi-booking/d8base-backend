# Generated by Django 3.0.5 on 2020-05-16 13:44

import d8b.services
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('professionals', '0015_professionalcertificate'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfessionalPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='name')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='description')),
                ('order', models.PositiveIntegerField(db_index=True, default=0)),
                ('photo', imagekit.models.fields.ProcessedImageField(upload_to=d8b.services.RandomFilenameGenerator('photos', 'professional'))),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='professionals_professionalphoto_created_by', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='professionals_professionalphoto_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='modified by')),
                ('professional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='professionals.Professional', verbose_name='professional')),
            ],
            options={
                'ordering': ('order', '-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
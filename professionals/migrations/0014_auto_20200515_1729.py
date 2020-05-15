# Generated by Django 3.0.5 on 2020-05-15 17:29

import d8b.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('professionals', '0013_professional_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_de',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_en',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_fr',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_ru',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='professional',
            name='experience',
            field=models.PositiveSmallIntegerField(blank=True, db_index=True, null=True, verbose_name='years of experience'),
        ),
        migrations.AlterField(
            model_name='professional',
            name='is_auto_order_confirmation',
            field=models.BooleanField(db_index=True, default=True, help_text='are orders confirmed automatically?', verbose_name='is auto order confirmation?'),
        ),
        migrations.AlterField(
            model_name='professional',
            name='level',
            field=models.CharField(blank=True, choices=[('junior', 'junior'), ('middle', 'middle'), ('senior', 'senior')], db_index=True, max_length=20, null=True, verbose_name='level'),
        ),
        migrations.AlterField(
            model_name='professional',
            name='name',
            field=models.CharField(db_index=True, max_length=255, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='professionalcontact',
            name='value',
            field=models.CharField(db_index=True, max_length=255, verbose_name='value'),
        ),
        migrations.AlterField(
            model_name='professionallocation',
            name='is_default',
            field=models.BooleanField(db_index=True, default=False, help_text='is default location?', verbose_name='is default'),
        ),
        migrations.AlterField(
            model_name='professionaltag',
            name='name',
            field=models.CharField(db_index=True, max_length=255, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='name',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='name_de',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='name_en',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='name_fr',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='name_ru',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='name'),
        ),
        migrations.CreateModel(
            name='ProfessionalExperience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('company', models.CharField(max_length=255, verbose_name='company')),
                ('is_still_here', models.BooleanField(default=False, help_text='Is the professional still working here?', verbose_name='is_still_here')),
                ('start_date', models.DateField(blank=True, null=True, validators=[d8b.validators.validate_date_in_past], verbose_name='start date')),
                ('end_date', models.DateField(blank=True, null=True, validators=[d8b.validators.validate_date_in_past], verbose_name='end date')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='professionals_professionalexperience_created_by', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='professionals_professionalexperience_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='modified by')),
                ('professional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experience_entries', to='professionals.Professional', verbose_name='professional')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]

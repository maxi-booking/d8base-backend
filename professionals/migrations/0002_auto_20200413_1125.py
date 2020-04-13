# Generated by Django 2.2.11 on 2020-04-13 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('professionals', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('order',), 'verbose_name_plural': 'categories'},
        ),
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='category',
            name='description_de',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='category',
            name='description_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='category',
            name='description_fr',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='category',
            name='description_ru',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='category',
            name='name_de',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='category',
            name='name_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='category',
            name='name_fr',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='category',
            name='name_ru',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='description_de',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='description_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='description_fr',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='description_ru',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='name_de',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='name_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='name_fr',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='name_ru',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='name'),
        ),
    ]
# Generated by Django 3.0.5 on 2020-04-27 16:09

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0003_delete_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='seotag',
            name='podcast_description',
            field=models.TextField(blank=True, null=True, verbose_name='description подкастов'),
        ),
        migrations.AddField(
            model_name='seotag',
            name='podcast_keywords',
            field=models.TextField(blank=True, null=True, verbose_name='keywords подкастов'),
        ),
        migrations.AddField(
            model_name='seotag',
            name='podcast_seo',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='СЕО текст подкастов'),
        ),
        migrations.AddField(
            model_name='seotag',
            name='podcast_title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Title подкастов'),
        ),
        migrations.AddField(
            model_name='seotag',
            name='recomended_description',
            field=models.TextField(blank=True, null=True, verbose_name='description рекомендаций'),
        ),
        migrations.AddField(
            model_name='seotag',
            name='recomended_keywords',
            field=models.TextField(blank=True, null=True, verbose_name='keywords рекомендаций'),
        ),
        migrations.AddField(
            model_name='seotag',
            name='recomended_seo',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='СЕО текст рекомендаций'),
        ),
        migrations.AddField(
            model_name='seotag',
            name='recomended_title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Title рекомендаций'),
        ),
        migrations.AddField(
            model_name='seotag',
            name='trends_description',
            field=models.TextField(blank=True, null=True, verbose_name='description трендов'),
        ),
        migrations.AddField(
            model_name='seotag',
            name='trends_keywords',
            field=models.TextField(blank=True, null=True, verbose_name='keywords трендов'),
        ),
        migrations.AddField(
            model_name='seotag',
            name='trends_seo',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='СЕО текст трендов'),
        ),
        migrations.AddField(
            model_name='seotag',
            name='trends_title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Title трендов'),
        ),
    ]

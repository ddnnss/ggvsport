# Generated by Django 3.0.5 on 2020-04-07 19:57

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Категория')),
                ('name_lower', models.CharField(blank=True, db_index=True, editable=False, max_length=255, null=True)),
                ('name_slug', models.CharField(blank=True, db_index=True, editable=False, max_length=255, null=True)),
                ('image', models.ImageField(null=True, upload_to='category/', verbose_name='Изображение (420 x 225)')),
                ('page_h1', models.CharField(blank=True, max_length=255, null=True, verbose_name='Тег H1 (если не указан, выводится название категории)')),
                ('page_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название страницы SEO')),
                ('page_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Описание страницы SEO')),
                ('page_keywords', models.TextField(blank=True, null=True, verbose_name='Keywords SEO')),
                ('seo_text', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='СЕО текст на страницу')),
                ('views', models.IntegerField(blank=True, default=0, verbose_name='Просмотров категории')),
                ('is_active', models.BooleanField(default=True, verbose_name='Отображается на сайте?')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Подкатегория')),
                ('name_lower', models.CharField(blank=True, db_index=True, editable=False, max_length=255, null=True)),
                ('name_slug', models.CharField(blank=True, db_index=True, editable=False, max_length=255, null=True)),
                ('image', models.ImageField(null=True, upload_to='subcategory/', verbose_name='Изображение (420 x 225)')),
                ('page_h1', models.CharField(blank=True, max_length=255, null=True, verbose_name='Тег H1 (если не указан, выводится название подкатегории)')),
                ('page_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название страницы SEO')),
                ('page_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Описание страницы SEO')),
                ('page_keywords', models.TextField(blank=True, null=True, verbose_name='Keywords SEO')),
                ('seo_text', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='СЕО текст на страницу')),
                ('views', models.IntegerField(blank=True, default=0, verbose_name='Просмотров подкатегории')),
                ('is_active', models.BooleanField(default=True, verbose_name='Отображается на сайте?')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='category.Category', verbose_name='Относится к ')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
    ]

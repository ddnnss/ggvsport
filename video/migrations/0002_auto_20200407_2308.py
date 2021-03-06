# Generated by Django 3.0.5 on 2020-04-07 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_auto_20200407_2308'),
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='video',
            options={'verbose_name': 'Видео', 'verbose_name_plural': 'Видео'},
        ),
        migrations.AddField(
            model_name='video',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='category.Category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='video',
            name='subcategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='category.SubCategory', verbose_name='Подкатегория'),
        ),
        migrations.AlterField(
            model_name='video',
            name='name',
            field=models.CharField(max_length=255, null=True, verbose_name='Название'),
        ),
    ]

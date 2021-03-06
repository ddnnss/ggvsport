# Generated by Django 2.2.7 on 2020-04-23 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_auto_20200413_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='category/', verbose_name='Изображение (420 x 225)'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcat', to='category.Category', verbose_name='Относится к '),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='subcategory/', verbose_name='Изображение (420 x 225)'),
        ),
    ]

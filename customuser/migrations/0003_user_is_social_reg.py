# Generated by Django 2.2.7 on 2020-04-13 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0002_auto_20200412_2221'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_social_reg',
            field=models.BooleanField(default=True),
        ),
    ]

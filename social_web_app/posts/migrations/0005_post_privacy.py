# Generated by Django 3.0.1 on 2019-12-29 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20191229_1207'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='privacy',
            field=models.BooleanField(default=True),
        ),
    ]

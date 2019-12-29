# Generated by Django 3.0.1 on 2019-12-29 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='like',
            name='post',
        ),
        migrations.AddField(
            model_name='like',
            name='owner_id',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='like',
            name='post_id',
            field=models.CharField(max_length=10, null=True),
        ),
    ]

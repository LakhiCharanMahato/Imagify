# Generated by Django 3.2.12 on 2022-03-15 03:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ladders', '0006_ladder_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ladder',
            name='user_name',
        ),
    ]

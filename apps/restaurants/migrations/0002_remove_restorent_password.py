# Generated by Django 4.1.4 on 2023-01-26 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='password',
        ),
    ]
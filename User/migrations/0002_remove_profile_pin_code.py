# Generated by Django 5.0.4 on 2024-04-28 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='pin_code',
        ),
    ]
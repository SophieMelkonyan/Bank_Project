# Generated by Django 5.0.4 on 2024-04-28 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_remove_profile_pin_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='pin_code',
            field=models.IntegerField(),
        ),
    ]

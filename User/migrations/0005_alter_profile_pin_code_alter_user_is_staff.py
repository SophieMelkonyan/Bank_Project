# Generated by Django 5.0.4 on 2024-04-29 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0004_remove_user_is_customer_remove_user_pin_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pin_code',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]

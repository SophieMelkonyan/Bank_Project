# Generated by Django 5.0.4 on 2024-04-23 08:36

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('service_id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(default='', max_length=10)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('number', models.IntegerField(default=0)),
                ('windows', models.IntegerField(default=0)),
                ('number1_available', models.BooleanField(default=True)),
                ('number2_available', models.BooleanField(default=True)),
            ],
        ),
    ]
# Generated by Django 5.0.3 on 2024-08-27 17:19

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting_app', '0004_policy'),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', tinymce.models.HTMLField()),
            ],
        ),
    ]

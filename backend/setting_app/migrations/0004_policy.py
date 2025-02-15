# Generated by Django 5.0.3 on 2024-08-26 20:57

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting_app', '0003_rename_post_terms'),
    ]

    operations = [
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('privacy_policy', tinymce.models.HTMLField()),
            ],
        ),
    ]

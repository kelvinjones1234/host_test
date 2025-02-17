# Generated by Django 5.1 on 2024-08-11 16:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AirtimeSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('network', models.CharField(blank=True, max_length=100, null=True)),
                ('network_id', models.PositiveIntegerField(default=1)),
                ('airtime_type', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Airtime Settings',
            },
        ),
        migrations.CreateModel(
            name='CableSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cable_name', models.CharField(max_length=100, verbose_name='Cable Name')),
                ('cable_id', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Cable Settings',
            },
        ),
        migrations.CreateModel(
            name='DataSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('network', models.CharField(blank=True, max_length=100, null=True)),
                ('network_id', models.PositiveIntegerField(default=1)),
                ('plan_type', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Data Settings',
            },
        ),
        migrations.CreateModel(
            name='ElectricitySettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meter_type', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Electricity Settings',
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
                ('image', models.FileField(blank=True, null=True, upload_to='svgs')),
            ],
            options={
                'verbose_name': 'Product Category',
            },
        ),
        migrations.CreateModel(
            name='Epin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_type', models.CharField(max_length=200)),
                ('price', models.PositiveBigIntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.productcategory')),
            ],
            options={
                'verbose_name_plural': 'E-Pin',
            },
        ),
        migrations.CreateModel(
            name='Electricity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_id', models.PositiveIntegerField(default=1)),
                ('disco_name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('meter_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.electricitysettings')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.productcategory')),
            ],
            options={
                'verbose_name_plural': 'Electricity',
            },
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('network', models.CharField(choices=[('mtn', 'MTN'), ('glo', 'GLO'), ('airtel', 'AIRTEL'), ('9mobile', '9MOBILE')], max_length=10)),
                ('plan_id', models.PositiveIntegerField(default=1)),
                ('data_plan', models.CharField(max_length=50)),
                ('price', models.PositiveBigIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('plan_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.datasettings')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.productcategory')),
            ],
            options={
                'verbose_name_plural': 'Data',
            },
        ),
        migrations.CreateModel(
            name='Cable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cable_plan', models.CharField(max_length=300)),
                ('plan_id', models.PositiveIntegerField(default=0)),
                ('price', models.CharField(max_length=10)),
                ('cable_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.cablesettings')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.productcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Airtime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('network', models.CharField(choices=[('mtn', 'MTN'), ('glo', 'GLO'), ('airtel', 'AIRTEL'), ('9mobile', '9MOBILE')], max_length=10)),
                ('airtime_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.airtimesettings')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.productcategory')),
            ],
            options={
                'verbose_name_plural': 'Airtime',
            },
        ),
    ]

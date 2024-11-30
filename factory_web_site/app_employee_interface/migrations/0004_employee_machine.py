# Generated by Django 4.2.16 on 2024-11-29 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_employee_interface', '0003_alter_vendor_options_material'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField()),
                ('specialty', models.CharField()),
            ],
            options={
                'ordering': ['full_name'],
            },
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField()),
                ('machine_name', models.CharField()),
                ('specialty', models.CharField()),
            ],
            options={
                'ordering': ['serial_number'],
            },
        ),
    ]

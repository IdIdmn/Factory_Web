# Generated by Django 4.2.16 on 2024-11-29 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_employee_interface', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vendor',
            old_name='name',
            new_name='company_name',
        ),
    ]

# Generated by Django 4.2.16 on 2024-12-01 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_client_interface', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='На рассмотрении'),
        ),
    ]

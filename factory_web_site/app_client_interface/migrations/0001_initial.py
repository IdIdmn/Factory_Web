# Generated by Django 4.2.16 on 2024-11-18 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('order_type', models.CharField(max_length=50)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('files', models.FileField(blank=True, null=True, upload_to='projects_store')),
            ],
        ),
    ]

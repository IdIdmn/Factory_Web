# Generated by Django 4.2.16 on 2024-11-29 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_employee_interface', '0002_rename_name_vendor_company_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vendor',
            options={'ordering': ['company_name']},
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metal_type', models.CharField()),
                ('metal_grade', models.CharField()),
                ('cost', models.FloatField()),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='app_employee_interface.vendor')),
            ],
        ),
    ]
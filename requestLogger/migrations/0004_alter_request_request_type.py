# Generated by Django 4.2.3 on 2023-08-03 17:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("requestLogger", "0003_request_date_completed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="request",
            name="request_type",
            field=models.CharField(
                choices=[("Change", "Change"), ("Service Request", "Service Request")],
                default="Service Request",
                max_length=15,
            ),
        ),
    ]
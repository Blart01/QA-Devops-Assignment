# Generated by Django 4.2.3 on 2023-08-02 21:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("requestLogger", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="status",
            field=models.CharField(
                choices=[
                    ("Active", "Active"),
                    ("Inactive", "Inactive"),
                    ("Deprecated", "Deprecated"),
                ],
                default="Active",
                max_length=50,
            ),
        ),
    ]

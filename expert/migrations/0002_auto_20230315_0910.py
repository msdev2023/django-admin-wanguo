# Generated by Django 3.2.18 on 2023-03-15 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("expert", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="expert",
            name="company",
            field=models.CharField(default="", max_length=128, verbose_name="Company"),
        ),
        migrations.CreateModel(
            name="ProjectBlackList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "company",
                    models.CharField(
                        max_length=128, verbose_name="Select a company to block"
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="expert.project"
                    ),
                ),
            ],
        ),
    ]

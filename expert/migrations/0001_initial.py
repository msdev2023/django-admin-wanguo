# Generated by Django 3.2.16 on 2023-03-13 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Expert",
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
                    "username",
                    models.CharField(
                        db_index=True, max_length=32, verbose_name="User Name"
                    ),
                ),
                (
                    "phone",
                    models.BigIntegerField(db_index=True, verbose_name="Phone Number"),
                ),
                (
                    "weight",
                    models.SmallIntegerField(
                        choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (9999, 5)],
                        default=1,
                        help_text="The higher the number, the higher the probability of being selected",
                        verbose_name="Weight",
                    ),
                ),
            ],
            options={
                "verbose_name": "Expert",
                "verbose_name_plural": "Experts",
            },
        ),
        migrations.CreateModel(
            name="Project",
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
                    "name",
                    models.CharField(
                        max_length=128, unique=True, verbose_name="Project Name"
                    ),
                ),
            ],
            options={
                "verbose_name": "Project",
                "verbose_name_plural": "Projects",
            },
        ),
        migrations.CreateModel(
            name="Sector",
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
                    "name",
                    models.CharField(
                        max_length=64, unique=True, verbose_name="Sector Name"
                    ),
                ),
            ],
            options={
                "verbose_name": "Sector",
                "verbose_name_plural": "Sectors",
            },
        ),
        migrations.CreateModel(
            name="ProjectItem",
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
                    "count",
                    models.PositiveIntegerField(
                        verbose_name="Select the number of experts"
                    ),
                ),
                ("experts", models.ManyToManyField(to="expert.Expert")),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="expert.project"
                    ),
                ),
                (
                    "sector",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="expert.sector",
                        verbose_name="Select a sector",
                    ),
                ),
            ],
            options={
                "verbose_name": "Project Item",
                "verbose_name_plural": "Project Items",
            },
        ),
        migrations.AddField(
            model_name="expert",
            name="sector",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="expert.sector",
                verbose_name="Sector",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="expert",
            unique_together={("username", "phone")},
        ),
    ]

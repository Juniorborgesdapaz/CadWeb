# Generated by Django 4.2.16 on 2025-01-08 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cliente",
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
                ("nome", models.CharField(max_length=100)),
                ("cpf", models.CharField(max_length=15, verbose_name="C.P.F")),
                ("datanasc", models.DateField(verbose_name="Data de Nascimento")),
            ],
        ),
    ]

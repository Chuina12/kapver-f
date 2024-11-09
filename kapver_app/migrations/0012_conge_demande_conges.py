# Generated by Django 5.0.1 on 2024-04-09 23:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kapver_app", "0011_dokumente"),
    ]

    operations = [
        migrations.CreateModel(
            name="Conge",
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
                    models.CharField(max_length=100, verbose_name="Name, Vorname"),
                ),
                ("geb", models.DateField(verbose_name="Geb. am")),
                (
                    "personalnummer",
                    models.CharField(max_length=100, verbose_name="Personalnummer"),
                ),
                ("von", models.DateField(verbose_name="Urlaubsantrag vom")),
                ("bis", models.DateField(verbose_name="bis")),
                (
                    "resturlaub",
                    models.CharField(
                        max_length=100, verbose_name="Tage aus dem Vorjahr (Resturlaub)"
                    ),
                ),
                (
                    "diesesjahr",
                    models.IntegerField(verbose_name="Tage aus diesem Jahr"),
                ),
                ("datum_antrag", models.DateField(verbose_name="Datum des Antrags")),
                (
                    "unterschrift_arbeitnehmer",
                    models.CharField(
                        max_length=100, verbose_name="Unterschrift des Arbeitnehmers"
                    ),
                ),
                (
                    "begrundung_arbeitgeber",
                    models.TextField(verbose_name="Antwort des Arbeitgebers"),
                ),
                (
                    "unterschrift_arbeitgeber",
                    models.CharField(
                        max_length=100, verbose_name="Unterschrift des Arbeitgebers"
                    ),
                ),
                (
                    "employer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="kapver_app.employer",
                    ),
                ),
                (
                    "entreprise",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="kapver_app.entreprise",
                    ),
                ),
            ],
            options={
                "verbose_name": "Conge",
                "verbose_name_plural": "Conges",
            },
        ),
        migrations.CreateModel(
            name="Demande_conges",
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
                ("demande", models.FileField(upload_to="demande")),
                ("date", models.DateField(auto_now_add=True)),
                ("reponse", models.BooleanField(default=False)),
                (
                    "employer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="kapver_app.employer",
                    ),
                ),
                (
                    "entreprise",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="kapver_app.entreprise",
                    ),
                ),
            ],
            options={
                "verbose_name": "Demande_conge",
                "verbose_name_plural": "Demande_conges",
            },
        ),
    ]

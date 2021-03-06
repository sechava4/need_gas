# Generated by Django 3.2.6 on 2021-09-02 07:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("need_gas_app", "0010_alter_client_y"),
    ]

    operations = [
        migrations.CreateModel(
            name="Driver",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                (
                    "x",
                    models.FloatField(
                        max_length=5,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                    ),
                ),
                (
                    "y",
                    models.FloatField(
                        max_length=5,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                    ),
                ),
                ("updated", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name="client",
            name="x",
            field=models.FloatField(
                max_length=5,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(100),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="client",
            name="y",
            field=models.FloatField(
                max_length=5,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(100),
                ],
            ),
        ),
    ]

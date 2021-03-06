# Generated by Django 3.2.6 on 2021-09-03 03:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("need_gas_app", "0011_auto_20210902_0240"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="driver",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="services",
                to="need_gas_app.driver",
            ),
            preserve_default=False,
        ),
    ]

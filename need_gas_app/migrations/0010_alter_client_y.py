# Generated by Django 3.2.6 on 2021-09-02 04:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('need_gas_app', '0009_alter_client_x'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='y',
            field=models.FloatField(max_length=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)]),
        ),
    ]

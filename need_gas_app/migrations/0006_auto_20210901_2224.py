# Generated by Django 3.2.6 on 2021-09-02 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('need_gas_app', '0005_auto_20210901_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='service',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
    ]
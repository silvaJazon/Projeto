# Generated by Django 5.0 on 2024-02-16 21:19

import inventory_english.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_english', '0003_materialquantityperunit_minimum_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialquantityperunit',
            name='stock_level',
            field=models.CharField(choices=[('normal', 'NORMAL'), ('critical', 'CRITICAL')], default=inventory_english.models.StockLevel['NORMAL'], max_length=20),
        ),
    ]
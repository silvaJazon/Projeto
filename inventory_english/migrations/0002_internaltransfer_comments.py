# Generated by Django 5.0 on 2024-02-16 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_english', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='internaltransfer',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
    ]

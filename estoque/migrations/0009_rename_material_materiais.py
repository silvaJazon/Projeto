# Generated by Django 5.0 on 2023-12-21 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0008_alter_saidamaterial_destino'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Material',
            new_name='Materiais',
        ),
    ]

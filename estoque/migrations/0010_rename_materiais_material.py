# Generated by Django 5.0 on 2023-12-21 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0009_rename_material_materiais'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Materiais',
            new_name='Material',
        ),
    ]

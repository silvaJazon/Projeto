# Generated by Django 5.0 on 2024-01-26 23:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0034_entradamaterial_confirmado'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoria',
            options={'verbose_name': 'Categoria do material', 'verbose_name_plural': 'Categoria dos materiais'},
        ),
        migrations.RemoveField(
            model_name='entradamaterial',
            name='confirmado',
        ),
        migrations.RemoveField(
            model_name='materiais',
            name='em_estoque',
        ),
    ]

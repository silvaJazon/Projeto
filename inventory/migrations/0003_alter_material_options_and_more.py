# Generated by Django 5.0 on 2024-02-07 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_alter_quantidadematerialporunidade_quantidade_em_estoque'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='material',
            options={'verbose_name': 'Material', 'verbose_name_plural': 'Materiais'},
        ),
        migrations.AlterModelOptions(
            name='quantidadematerialporunidade',
            options={'verbose_name': 'Estoque por Unidade', 'verbose_name_plural': 'Estoque por Unidades'},
        ),
    ]
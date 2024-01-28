# Generated by Django 5.0 on 2024-01-22 16:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0016_entradamaterial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoria',
            options={'verbose_name': 'Categoria do material', 'verbose_name_plural': ' Categoria dos materiais'},
        ),
        migrations.AddField(
            model_name='entradamaterial',
            name='remetente',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='itenspacote',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estoque.materiais', verbose_name='Material'),
        ),
        migrations.AlterField(
            model_name='itenspacote',
            name='pacote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estoque.pacote', verbose_name='Pacote'),
        ),
        migrations.AlterField(
            model_name='materiais',
            name='nome',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]

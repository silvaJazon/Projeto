# Generated by Django 5.0 on 2024-02-02 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_alter_quantidadematerialunidade_quantidade'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unidadearm',
            name='materiais',
        ),
        migrations.RemoveField(
            model_name='materiais',
            name='quantidade_total',
        ),
        migrations.AddField(
            model_name='materiais',
            name='quantidade_em_estoque',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='unidadearm',
            name='data_encerramento',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data de encerramneto da Unidade de Armazenamento'),
        ),
        migrations.DeleteModel(
            name='QuantidadeMaterialUnidade',
        ),
    ]

# Generated by Django 5.0 on 2024-01-29 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0037_remove_materiais_unidades_armazenamento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='nome',
            field=models.CharField(choices=[('FERRAMENTAS', 'Ferramentas'), ('MASTROS', 'Mastros'), ('BATERIAS', 'Baterias'), ('ACESSORIOS', 'Acessórios'), ('CABOS', 'Cabos'), ('ANTENAS', 'Antenas'), ('PORCAS_E_PARAFUSOS', 'Porcas e Parafusos'), ('CONECTORES_PINOS_BARRAMENTOS', 'Conectores, Pinos e Barramentos'), ('SENSORES', 'Sensores'), ('PLACAS_E_ELETRONICOS', 'Placas e Eletrônicos'), ('OUTROS', 'Outros')], max_length=50),
        ),
        migrations.AlterField(
            model_name='materiais',
            name='categoria',
            field=models.CharField(blank=True, choices=[('FERRAMENTAS', 'Ferramentas'), ('MASTROS', 'Mastros'), ('BATERIAS', 'Baterias'), ('ACESSORIOS', 'Acessórios'), ('CABOS', 'Cabos'), ('ANTENAS', 'Antenas'), ('PORCAS_E_PARAFUSOS', 'Porcas e Parafusos'), ('CONECTORES_PINOS_BARRAMENTOS', 'Conectores, Pinos e Barramentos'), ('SENSORES', 'Sensores'), ('PLACAS_E_ELETRONICOS', 'Placas e Eletrônicos'), ('OUTROS', 'Outros')], max_length=50, null=True),
        ),
    ]

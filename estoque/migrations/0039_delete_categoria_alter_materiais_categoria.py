# Generated by Django 5.0 on 2024-01-30 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0038_alter_categoria_nome_alter_materiais_categoria'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Categoria',
        ),
        migrations.AlterField(
            model_name='materiais',
            name='categoria',
            field=models.CharField(blank=True, choices=[('FERRAMENTAS', 'Ferramentas'), ('MASTROS', 'Mastros'), ('BATERIAS', 'Baterias'), ('ACESSORIOS', 'Acessórios'), ('CABOS', 'Cabos'), ('ANTENAS', 'Antenas'), ('PORCAS_E_PARAFUSOS', 'Porcas e Parafusos'), ('CONECTORES_PINOS_BARRAMENTOS', 'Conectores, Pinos e Barramentos'), ('SENSORES', 'Sensores'), ('PLACAS_E_ELETRONICOS', 'Placas e Eletrônicos'), ('SUPORTE', 'Suportes'), ('OUTROS', 'Outros')], max_length=50, null=True),
        ),
    ]

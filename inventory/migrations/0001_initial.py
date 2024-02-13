# Generated by Django 5.0 on 2024-02-06 15:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True)),
                ('categoria', models.CharField(blank=True, choices=[('FERRAMENTAS', 'Ferramentas'), ('MASTROS', 'Mastros'), ('BATERIAS', 'Baterias'), ('ACESSORIOS', 'Acessórios'), ('CABOS', 'Cabos'), ('ANTENAS', 'Antenas'), ('PORCAS_E_PARAFUSOS', 'Porcas e Parafusos'), ('CONECTORES_PINOS_BARRAMENTOS', 'Conectores, Pinos e Barramentos'), ('SENSORES', 'Sensores'), ('PLACAS_E_ELETRONICOS', 'Placas e Eletrônicos'), ('SUPORTE', 'Suportes'), ('OUTROS', 'Outros')], max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Material em estoque',
                'verbose_name_plural': 'Materiais em estoque',
            },
        ),
        migrations.CreateModel(
            name='UnidadeArm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, null=True, unique=True)),
                ('responsavel', models.CharField(max_length=50, null=True, unique=True)),
                ('is_ativo', models.BooleanField(null=True, verbose_name='Está ativa?')),
                ('data_ativacao', models.DateTimeField(null=True, verbose_name='Data de ativação da Unidade de Armazenamento')),
                ('data_encerramento', models.DateTimeField(blank=True, null=True, verbose_name='Data de encerramneto da Unidade de Armazenamento')),
            ],
            options={
                'verbose_name': 'Unidade de Armazenamento',
                'verbose_name_plural': 'Unidades de Armazenamento',
            },
        ),
        migrations.CreateModel(
            name='ItensPacote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField()),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.material', verbose_name='Material')),
            ],
        ),
        migrations.CreateModel(
            name='Pacote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('materiais', models.ManyToManyField(through='inventory.ItensPacote', to='inventory.material')),
            ],
        ),
        migrations.AddField(
            model_name='itenspacote',
            name='pacote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.pacote', verbose_name='Pacote'),
        ),
        migrations.CreateModel(
            name='SaidaMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_saida', models.DateTimeField(auto_now_add=True)),
                ('destino', models.CharField(max_length=100, null=True)),
                ('servico', models.CharField(choices=[('Instalação', 'Instalação'), ('Manutenção Preventiva', 'Manutenção Preventiva'), ('Manutenção Corretiva', 'Manutenção Corretiva')], max_length=100)),
                ('pacote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.pacote')),
                ('unidade_debito', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.unidadearm')),
            ],
            options={
                'verbose_name': 'Registro de saída de Material',
                'verbose_name_plural': 'Registros de saídas de Materiais',
            },
        ),
        migrations.CreateModel(
            name='QuantidadeMaterialPorUnidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade_em_estoque', models.PositiveIntegerField()),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.material')),
                ('unidade', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.unidadearm')),
            ],
            options={
                'verbose_name': 'Quantidade por Unidade',
                'verbose_name_plural': 'Quantidade por Unidades',
            },
        ),
        migrations.CreateModel(
            name='EntradaMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField()),
                ('data_entrada', models.DateTimeField(auto_now_add=True)),
                ('remetente', models.CharField(max_length=100, null=True)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.material')),
                ('destino', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.unidadearm')),
            ],
            options={
                'verbose_name': 'Registro de entrada de Material',
                'verbose_name_plural': 'Registros de entradas de Materiais',
            },
        ),
    ]
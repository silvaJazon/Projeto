# Generated by Django 5.0 on 2023-12-21 16:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0002_remove_produto_categoria_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('quantidade_em_estoque', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ItensPacote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField()),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estoque.material')),
            ],
        ),
        migrations.CreateModel(
            name='Pacote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('materiais', models.ManyToManyField(through='estoque.ItensPacote', to='estoque.material')),
            ],
        ),
        migrations.AddField(
            model_name='itenspacote',
            name='pacote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estoque.pacote'),
        ),
        migrations.CreateModel(
            name='SaidaMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_saida', models.DateTimeField(auto_now_add=True)),
                ('pacote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estoque.pacote')),
            ],
        ),
        migrations.DeleteModel(
            name='Estacao',
        ),
        migrations.DeleteModel(
            name='Produto',
        ),
    ]

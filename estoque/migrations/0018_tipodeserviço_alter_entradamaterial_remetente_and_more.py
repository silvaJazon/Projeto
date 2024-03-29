# Generated by Django 5.0 on 2024-01-22 17:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0017_alter_categoria_options_entradamaterial_remetente_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoDeServiço',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='entradamaterial',
            name='remetente',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='saidamaterial',
            name='destino',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='saidamaterial',
            name='tipo_de_servico',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='estoque.tipodeserviço'),
        ),
    ]

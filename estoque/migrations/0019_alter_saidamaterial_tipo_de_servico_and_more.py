# Generated by Django 5.0 on 2024-01-22 18:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0018_tipodeserviço_alter_entradamaterial_remetente_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saidamaterial',
            name='tipo_de_servico',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='estoque.tipodeserviço'),
        ),
        migrations.AlterField(
            model_name='tipodeserviço',
            name='tipo',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]

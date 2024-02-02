# Generated by Django 5.0 on 2024-02-02 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0043_responsavel_is_ativo_alter_responsavel_data_ativacao'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='responsavel',
            name='is_ativo',
        ),
        migrations.AddField(
            model_name='responsavel',
            name='data_encerramento',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data de encerramento do usuário'),
        ),
    ]

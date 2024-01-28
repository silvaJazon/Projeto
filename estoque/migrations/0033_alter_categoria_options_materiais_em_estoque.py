# Generated by Django 5.0 on 2024-01-26 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0032_alter_saidamaterial_servico_alter_categoria_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoria',
            options={'verbose_name': 'Categoria do material', 'verbose_name_plural': 'Categorias dos materiais'},
        ),
        migrations.AddField(
            model_name='materiais',
            name='em_estoque',
            field=models.BooleanField(default=True),
        ),
    ]

# Generated by Django 5.0 on 2023-12-21 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0003_material_itenspacote_pacote_itenspacote_pacote_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='saidamaterial',
            name='destino',
            field=models.CharField(default=None, max_length=100),
        ),
    ]

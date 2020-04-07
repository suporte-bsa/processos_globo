# Generated by Django 2.2.12 on 2020-04-02 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consulta_a_processos', '0005_auto_20200402_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='processos',
            name='data_atualizacao',
            field=models.TextField(blank=True, default='02/04/2020', null=True),
        ),
        migrations.AddField(
            model_name='processos',
            name='descricao_atualizacao',
            field=models.TextField(blank=True, default='desc_at', null=True),
        ),
        migrations.AddField(
            model_name='processos',
            name='incidente_id',
            field=models.TextField(blank=True, default='id', null=True),
        ),
        migrations.AlterField(
            model_name='processos',
            name='emails',
            field=models.TextField(blank=True, default='globomonitoracao@gmail.com', null=True),
        ),
    ]
# Generated by Django 2.2.12 on 2020-04-14 22:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('consulta_a_processos', '0009_auto_20200408_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processos',
            name='data_atualizacao',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]

# Generated by Django 5.0.9 on 2024-12-09 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr', '0014_alter_documentosocr_arquivo_existe_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogExclusoes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_documento', models.CharField(blank=True, max_length=18, null=True, verbose_name='Id')),
                ('numero_pagina', models.IntegerField(blank=True, default='N/A', null=True, verbose_name='Número da página')),
                ('data_exclusao', models.DateTimeField(auto_now_add=True, verbose_name='Data da exclusão')),
            ],
            options={
                'verbose_name': 'Log Exclusões',
                'verbose_name_plural': 'Log Exclusões',
            },
        ),
    ]
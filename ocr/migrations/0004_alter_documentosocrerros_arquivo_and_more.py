# Generated by Django 5.0.9 on 2024-10-07 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr', '0003_alter_documentosocr_arquivo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentosocrerros',
            name='arquivo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='documentosocrerros',
            name='caminho',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='documentosocrerros',
            name='nome_original',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='documentosocrerros',
            name='numero_pagina',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='documentosocrerros',
            name='pasta',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
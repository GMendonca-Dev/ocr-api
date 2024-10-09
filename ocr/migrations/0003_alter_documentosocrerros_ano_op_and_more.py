# Generated by Django 5.0.9 on 2024-10-09 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr', '0002_documentosocrerros_ano_op_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentosocrerros',
            name='ano_op',
            field=models.CharField(blank=True, default='N/A', max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='documentosocrerros',
            name='arquivo',
            field=models.CharField(blank=True, default='N/A', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='documentosocrerros',
            name='caminho',
            field=models.TextField(blank=True, default='N/A', null=True),
        ),
        migrations.AlterField(
            model_name='documentosocrerros',
            name='email_usuario',
            field=models.CharField(blank=True, default='N/A', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='documentosocrerros',
            name='erro',
            field=models.TextField(blank=True, default='N/A', null=True),
        ),
        migrations.AlterField(
            model_name='documentosocrerros',
            name='extensao_arquivo',
            field=models.CharField(blank=True, default='N/A', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='documentosocrerros',
            name='nome_original',
            field=models.CharField(blank=True, default='N/A', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='documentosocrerros',
            name='num_op',
            field=models.CharField(blank=True, default='N/A', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='documentosocrerros',
            name='numero_pagina',
            field=models.IntegerField(blank=True, default='N/A', null=True),
        ),
        migrations.AlterField(
            model_name='documentosocrerros',
            name='pasta',
            field=models.CharField(blank=True, default='N/A', max_length=150, null=True),
        ),
    ]
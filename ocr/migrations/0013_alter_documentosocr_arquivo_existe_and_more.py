# Generated by Django 5.0.9 on 2024-11-22 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr', '0012_alter_documentosocr_arquivo_existe_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentosocr',
            name='arquivo_existe',
            field=models.IntegerField(blank=True, default=1, null=True, verbose_name='Arquivo existe'),
        ),
        migrations.AlterField(
            model_name='documentosocrerros',
            name='arquivo_existe',
            field=models.IntegerField(blank=True, default=1, null=True, verbose_name='Arquivo existe'),
        ),
    ]

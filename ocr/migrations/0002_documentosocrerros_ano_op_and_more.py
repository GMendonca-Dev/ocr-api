# Generated by Django 5.0.9 on 2024-10-08 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentosocrerros',
            name='ano_op',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='documentosocrerros',
            name='email_usuario',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='documentosocrerros',
            name='num_op',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]

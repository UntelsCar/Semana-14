# Generated by Django 5.0.6 on 2024-06-30 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='articulo',
            name='imagen',
            field=models.ImageField(default='null', upload_to=''),
        ),
    ]

# Generated by Django 4.2.19 on 2025-03-21 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.TextField(default='', max_length=20000),
            preserve_default=False,
        ),
    ]

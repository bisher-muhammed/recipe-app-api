# Generated by Django 3.2.25 on 2025-03-17 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_recipe'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='title',
            field=models.CharField(default='exit', max_length=233),
            preserve_default=False,
        ),
    ]

# Generated by Django 3.2.6 on 2024-07-29 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20240729_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='hidden',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='projectfile',
            name='primary',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 4.1.5 on 2023-03-05 02:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('HMS_APP', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='room_description',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

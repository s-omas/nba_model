# Generated by Django 4.2.4 on 2023-08-22 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prob_model', '0007_mostrecentday'),
    ]

    operations = [
        migrations.AddField(
            model_name='mostrecentday',
            name='rd_id',
            field=models.IntegerField(default=0),
        ),
    ]
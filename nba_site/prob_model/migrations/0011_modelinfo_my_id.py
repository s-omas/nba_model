# Generated by Django 4.2.4 on 2023-08-25 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prob_model', '0010_modelinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelinfo',
            name='my_id',
            field=models.IntegerField(default=0),
        ),
    ]
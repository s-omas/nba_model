# Generated by Django 4.2.4 on 2023-08-25 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prob_model', '0009_game_isprocessed'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_hist', models.JSONField()),
                ('sim_info', models.JSONField()),
            ],
        ),
    ]

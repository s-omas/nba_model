# Generated by Django 4.2.4 on 2023-08-18 20:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prob_model', '0004_schedule_name_team_team_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='prediction',
            name='away_team_rating',
            field=models.FloatField(default=1000),
        ),
        migrations.AddField(
            model_name='prediction',
            name='away_team_variance',
            field=models.FloatField(default=100),
        ),
        migrations.AddField(
            model_name='prediction',
            name='home_team_rating',
            field=models.FloatField(default=1000),
        ),
        migrations.AddField(
            model_name='prediction',
            name='home_team_variance',
            field=models.FloatField(default=100),
        ),
        migrations.CreateModel(
            name='Sim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField(default=1000)),
                ('variance', models.FloatField(default=100)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_sim', to='prob_model.team')),
            ],
        ),
    ]

# Generated by Django 4.2.7 on 2024-04-23 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0005_invitation_groups'),
        ('experiments', '0073_load_openai_voices'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExperimentRoute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('keyword', models.CharField(max_length=128)),
                ('is_default', models.BooleanField(default=False)),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_links', to='experiments.experiment')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_links', to='experiments.experiment')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.team', verbose_name='Team')),
            ],
            options={
                'unique_together': {('parent', 'keyword'), ('parent', 'child')},
            },
        ),
        migrations.AddField(
            model_name='experiment',
            name='children',
            field=models.ManyToManyField(blank=True, related_name='parents', through='experiments.ExperimentRoute', to='experiments.experiment'),
        ),
    ]

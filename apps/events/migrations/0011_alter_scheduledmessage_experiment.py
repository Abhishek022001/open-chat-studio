# Generated by Django 4.2.11 on 2024-05-27 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0079_alter_participant_unique_together_and_more'),
        ('events', '0010_add_experiment_to_scheduled_messages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduledmessage',
            name='experiment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scheduled_messages', to='experiments.experiment'),
        ),
    ]

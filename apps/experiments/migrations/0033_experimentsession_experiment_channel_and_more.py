# Generated by Django 4.2 on 2023-10-11 07:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("channels", "0007_alter_experimentchannel_platform"),
        ("experiments", "0032_load_synthetic_voices"),
    ]

    operations = [
        migrations.AddField(
            model_name="experimentsession",
            name="experiment_channel",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="experiment_sessions",
                to="channels.experimentchannel",
            ),
        ),
        migrations.AddField(
            model_name="experimentsession",
            name="external_chat_id",
            field=models.CharField(blank=True, null=True),
        ),
    ]

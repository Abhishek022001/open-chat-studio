# Generated by Django 4.2.14 on 2024-08-02 00:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pipelines', '0003_pipelinerun_session'),
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('flow_id', models.CharField(db_index=True, max_length=128)),
                ('type', models.CharField(max_length=128)),
                ('label', models.CharField(blank=True, default='', max_length=128)),
                ('params', models.JSONField(default=dict)),
                ('pipeline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pipelines.pipeline')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

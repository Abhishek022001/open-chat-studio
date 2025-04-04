# Generated by Django 5.1.5 on 2025-02-19 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_providers', '0024_add_deepseek_models'),
    ]

    operations = [
        migrations.AlterField(
            model_name='llmprovider',
            name='type',
            field=models.CharField(choices=[('openai', 'OpenAI'), ('azure', 'Azure OpenAI'), ('anthropic', 'Anthropic'), ('groq', 'Groq'), ('perplexity', 'Perplexity'), ('deepseek', 'DeepSeek')], max_length=255),
        ),
        migrations.AlterField(
            model_name='llmprovidermodel',
            name='type',
            field=models.CharField(choices=[('openai', 'OpenAI'), ('azure', 'Azure OpenAI'), ('anthropic', 'Anthropic'), ('groq', 'Groq'), ('perplexity', 'Perplexity'), ('deepseek', 'DeepSeek')], max_length=255),
        ),
    ]

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('service_providers', '0026_add_google_gemini_models'),
    ]

    operations = [
        migrations.AlterField(
            model_name='llmprovider',
            name='type',
            field=models.CharField(
                choices=[
                    ('openai', 'OpenAI'),
                    ('azure', 'Azure OpenAI'),
                    ('anthropic', 'Anthropic'),
                    ('groq', 'Groq'),
                    ('perplexity', 'Perplexity'),
                    ('deepseek', 'DeepSeek'),
                    ('google_gemini', 'Google Gemini')
                ],
                max_length=255
            ),
        ),
        migrations.AlterField(
            model_name='llmprovidermodel',
            name='type',
            field=models.CharField(
                choices=[
                    ('openai', 'OpenAI'),
                    ('azure', 'Azure OpenAI'),
                    ('anthropic', 'Anthropic'),
                    ('groq', 'Groq'),
                    ('perplexity', 'Perplexity'),
                    ('deepseek', 'DeepSeek'),
                    ('google_gemini', 'Google Gemini')
                ],
                max_length=255
            ),
        ),
    ]
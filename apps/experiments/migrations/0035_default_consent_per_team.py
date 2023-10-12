# Generated by Django 4.2 on 2023-10-12 11:28

from django.db import migrations

DEFAULT_CONSENT_TEXT = """
Welcome to this chatbot built on Open Chat Studio! 

The Chatbot is provided "as-is" and "as available." Open Chat Studio makes no warranties,
express or implied, regarding the Chatbot's accuracy, completeness, or availability.

You use the chatbot at your own risk. Open Chat Studio shall not be liable for any harm
or damages that may result from your use of the chatbot.

You understand and agree that any reliance on the Chatbot's responses is solely at your own
discretion and risk.

By selecting “I Agree” below, you indicate that: 

* You have read and understood the above information.
* You voluntarily agree to try out this chatbot.
* You are 18 years or older.
"""


def create_default_consent_form(apps, schema_editor):
    Team = apps.get_model("teams", "Team")
    ConsentForm = apps.get_model("experiments", "ConsentForm")
    for team in Team.objects.all():
        ConsentForm.objects.get_or_create(
            team=team,
            is_default=True,
            defaults={
                "name": "Default Consent",
                "consent_text": DEFAULT_CONSENT_TEXT,
            }
        )


class Migration(migrations.Migration):
    dependencies = [
        ("experiments", "0034_consentform_team_experiment_team_and_more"),
    ]

    operations = [
        migrations.RunPython(create_default_consent_form)
    ]

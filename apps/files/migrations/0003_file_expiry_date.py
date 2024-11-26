# Generated by Django 5.1.2 on 2024-11-26 08:47

from django.db import migrations, models

def create_periodic_task(apps, schema_editor):
    IntervalSchedule = apps.get_model("django_celery_beat", "IntervalSchedule")
    PeriodicTask = apps.get_model("django_celery_beat", "PeriodicTask")

    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=1,
        period="days",
    )
    PeriodicTask.objects.get_or_create(
        name="files.tasks.clean_up_expired_files",
        task="apps.files.tasks.clean_up_expired_files",
        interval=schedule,
    )

def delete_periodic_task(apps, schema_editor):
    PeriodicTask = apps.get_model("django_celery_beat", "PeriodicTask")
    PeriodicTask.objects.filter(name="files.tasks.clean_up_expired_files").delete()

class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_external_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='expiry_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.RunPython(create_periodic_task, delete_periodic_task)
    ]

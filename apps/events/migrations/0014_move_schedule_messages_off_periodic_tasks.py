# Generated by Django 4.2.11 on 2024-07-12 14:50
from datetime import datetime, timedelta
from django.db import migrations
import json

from apps.events.models import EventAction, EventActionType, ScheduledMessage
from apps.experiments.models import ExperimentSession

def is_complete(task):
	return datetime.now() > task.expires

def calculate_next_run(task, current_time):
	delta = timedelta(seconds=task.interval.every.total_seconds())
	next_time = task.start_time
	while next_time <= current_time:
		next_time += delta
	return next_time

def get_interval_duration(interval):
    if not interval:
        return None
    if interval.period == 'seconds':
        return timedelta(seconds=interval.every)
    elif interval.period == 'minutes':
        return timedelta(minutes=interval.every)
    elif interval.period == 'hours':
        return timedelta(hours=interval.every)
    elif interval.period == 'days':
        return timedelta(days=interval.every)
    elif interval.period == 'weeks':
        return timedelta(weeks=interval.every)
    else:
        return None

def calculate_remaining_repetitions(task, current_time):
    interval_duration = get_interval_duration(task.interval)
    remaining_time = task.expires - current_time if task.expires else None
    if not remaining_time or not interval_duration:
        return 0
    remaining_repetitions = remaining_time / interval_duration
    return int(remaining_repetitions)

def calculate_total_triggers(task, current_time):
    interval_duration = get_interval_duration(task.interval)
    start_time = task.date_changed
    if not start_time or not interval_duration:
        return 0
    elapsed_time = current_time - start_time
    return int(elapsed_time / interval_duration)

def calc_schedule_components(periodic_task, current_time):
    if periodic_task.one_off:
        schedule = periodic_task.clocked
        frequency = 1
        time_period = None
        repetitions = 1
        next_trigger_date = schedule.clocked_time
        total_triggers = 0
    else:
        schedule = periodic_task.interval
        frequency = schedule.every
        time_period = schedule.period
        repetitions = calculate_remaining_repetitions(periodic_task, current_time)
        next_trigger_date = calculate_next_run(periodic_task, current_time)
        total_triggers = calculate_total_triggers(periodic_task, current_time)

    return frequency, time_period, repetitions, total_triggers, next_trigger_date


class Migration(migrations.Migration):
    def migrate_periodic_tasks(apps, schema_editor):
        ScheduledMessage = apps.get_model('events', 'ScheduledMessage')
        EventAction = apps.get_model('events', 'EventAction')
        Experiment = apps.get_model('experiments', 'Experiment')
        Participant = apps.get_model('experiments', 'Participant')
        PeriodicTask = apps.get_model('django_celery_beat', 'PeriodicTask')
        current_time = datetime.now()

        for task in PeriodicTask.objects.filter(name__startswith="reminder-", enabled=True):
            task_kwargs = json.loads(task.kwargs)
            participant_identifiers = task_kwargs["chat_ids"]
            message = task_kwargs["message"]
            experiment = Experiment.objects.filter(public_id=task_kwargs["experiment_public_id"])
            task_complete = current_time > task.expires

            if not experiment or task_complete:
                continue

            frequency, time_period, repetitions, total_triggers, next_trigger_date = calc_schedule_components(task, current_time)

            if repetitions == 0:
                continue

            event_action_params = {
                "name": "system-generated-event-action",
                "prompt_text": message,
                "frequency": frequency,
                "time_period": time_period,
                "repetitions": repetitions,
            }

            for identifier in participant_identifiers:
                participant = Participant.objects.get(team=experiment.team, identifier=identifier)
                ScheduledMessage.objects.create(
                    experiment=experiment,
                    participant=participant,
                    team=experiment.team,
                    action=None,
                    last_triggered_at=task.last_run_at,
                    next_trigger_date=next_trigger_date,
                    total_triggers=total_triggers,
                    custom_schedule_params=event_action_params,
                )

    dependencies = [
        ('events', '0013_alter_scheduledmessage_action'),
    ]

    operations = [
        migrations.RunPython(migrate_periodic_tasks, elidable=True),
    ]

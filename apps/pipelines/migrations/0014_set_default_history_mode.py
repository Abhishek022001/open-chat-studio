# Generated by Django 5.1.2 on 2025-03-21 05:59

from django.db import migrations
from apps.pipelines.models import PipelineChatHistoryModes
from apps.pipelines.nodes.nodes import LLMResponseWithPrompt, RouterNode

CHUNK_SIZE = 100

def _set_default_history_mode(apps, schema_editor):
    Node = apps.get_model('pipelines', 'Node')
    node_queryset = Node.objects.filter(type__in=[LLMResponseWithPrompt.__name__, RouterNode.__name__])
    nodes = []
    for node in node_queryset.iterator(chunk_size=CHUNK_SIZE):
        node.params['history_mode'] = PipelineChatHistoryModes.SUMMARIZE
        nodes.append(node)
        if len(nodes) == CHUNK_SIZE:
            Node.objects.bulk_update(nodes, ['params'])
            nodes = []
    
    Node.objects.bulk_update(nodes, ['params'])


class Migration(migrations.Migration):
    dependencies = [
        ('pipelines', '0013_cast_citations_enabled_params_to_bool'),
    ]

    operations = [
        migrations.RunPython(_set_default_history_mode, reverse_code=migrations.RunPython.noop),
    ]

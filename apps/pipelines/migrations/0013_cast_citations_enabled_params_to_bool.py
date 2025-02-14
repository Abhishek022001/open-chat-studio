# Generated by Django 5.1.5 on 2025-02-14 12:15

from django.db import migrations

def _cast_params_to_bool(apps, schema_editor):
    Node = apps.get_model("pipelines", "Node")
    
    updated_nodes = []
    for node in Node.objects.filter(type="AssistantNode"):
        if "citations_enabled" in node.params:
            if node.params["citations_enabled"] == "true":
                node.params["citations_enabled"] = True
            elif node.params["citations_enabled"] == "false":
                node.params["citations_enabled"] = False
            
            updated_nodes.append(node)

    Node.objects.bulk_update(updated_nodes, ["params"])

def _cast_params_to_str(apps, schema_editor):
    Node = apps.get_model("pipelines", "Node")

    updated_nodes = []
    for node in Node.objects.filter(type="AssistantNode"):
        if "citations_enabled" in node.params:
            if node.params["citations_enabled"] == True:
                node.params["citations_enabled"] = "true"
            elif node.params["citations_enabled"] == False:
                node.params["citations_enabled"] = "false"

            updated_nodes.append(node)

    Node.objects.bulk_update(updated_nodes, ["params"])


class Migration(migrations.Migration):

    dependencies = [
        ('pipelines', '0012_auto_20250116_1508'),
    ]

    operations = [
        migrations.RunPython(_cast_params_to_bool, reverse_code=_cast_params_to_str)
    ]

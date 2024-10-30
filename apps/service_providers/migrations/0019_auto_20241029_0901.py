# Generated by Django 5.1.2 on 2024-10-28 17:35
import logging

from collections import namedtuple
from django.db import migrations
from django.db.models import Q

logger = logging.getLogger(__name__)


def _create_llm_provider_models(apps, schema_editor):
    _create_default_llm_provider_models(apps, schema_editor)
    _create_custom_llm_provider_models(apps, schema_editor)

DefaultLlmProviderModel = namedtuple('DefaultLlmProviderModel', ["type", "name", "max_token_limit"])

DEFAULT_LLM_PROVIDER_MODELS = {
    DefaultLlmProviderModel("openai", "gpt-4o-mini", 8192),
    DefaultLlmProviderModel("anthropic", "claude", 8192),
}

def _create_default_llm_provider_models(apps, schema_editor):
    LlmProviderModel = apps.get_model("service_providers", "LlmProviderModel")
    for default_provider_model in DEFAULT_LLM_PROVIDER_MODELS:
        LlmProviderModel.objects.create(
            team=None,
            type=default_provider_model.type,
            name=default_provider_model.name,
            max_token_limit=default_provider_model.max_token_limit,
            supports_tool_calling=True,
        )
    # TODO: Get list of current global models

def _handle_pipeline_node(LlmProvider, LlmProviderModel, node):
    try:
        llm_provider_id = node.params['llm_provider_id']
        llm_model = node.params['llm_model']
    except KeyError as exc:
        logger.warn(f"Error occured while migrating node {node.id}: {exc}")
        return
    try:
        llm_provider = LlmProvider.objects.get(id=llm_provider_id)
    except LlmProvider.DoesNotExist:
        logger.warn(f"Could not find provider with id {llm_provider_id}")
        return

    try:
        global_provider_model = LlmProviderModel.objects.get(
            team__isnull=True,
            type=llm_provider.type,
            name=llm_model,
            max_token_limit=node.params.get("max_token_limit", 8192)
        )
        node.params['llm_provider_model_id'] = str(global_provider_model.id)
        node.save()
        return
    except LlmProviderModel.DoesNotExist:
        pass

    try:
        custom_provider_model = LlmProviderModel.objects.get(
            team=node.pipeline.team,
            type=llm_provider.type,
            name=llm_model,
            max_token_limit=node.params.get("max_token_limit", 8192)
        )
        node.params['llm_provider_model_id'] = str(custom_provider_model.id)
        node.save()
        return
    except LlmProviderModel.DoesNotExist:
        pass

    new_custom_provider_model = LlmProviderModel.objects.create(
        team=node.pipeline.team,
        type=llm_provider.type,
        name=llm_model,
        max_token_limit=node.params.get("max_token_limit", 8192),
    )
    node.params['llm_provider_model_id'] = str(new_custom_provider_model.id)
    node.save()


def _handle_analysis(LlmProviderModel, analysis):
    try:
        global_provider_model = LlmProviderModel.objects.get(
            team__isnull=True,
            type=analysis.llm_provider.type,
            name=analysis.llm_model,
        )
        analysis.llm_provider_model = global_provider_model
        analysis.save()
        return
    except LlmProviderModel.DoesNotExist:
        pass

    try:
        custom_provider_model = LlmProviderModel.objects.get(
            team=analysis.team,
            type=analysis.llm_provider.type,
            name=analysis.llm_model,
        )
        analysis.llm_provider_model = custom_provider_model
        analysis.save()
        return
    except LlmProviderModel.DoesNotExist:
        pass

    new_custom_provider_model = LlmProviderModel.objects.create(
        team=analysis.team,
        type=analysis.llm_provider.type,
        name=analysis.llm_model,
    )
    analysis.llm_provider_model = new_custom_provider_model
    analysis.save()

def _handle_assistant(LlmProviderModel, assistant):
    try:
        global_provider_model = LlmProviderModel.objects.get(
            team__isnull=True,
            type=assistant.llm_provider.type,
            name=assistant.llm_model,
        )
        assistant.llm_provider_model = global_provider_model
        assistant.save()
        return
    except LlmProviderModel.DoesNotExist:
        pass

    try:
        custom_provider_model = LlmProviderModel.objects.get(
            team=assistant.team,
            type=assistant.llm_provider.type,
            name=assistant.llm_model,
        )
        assistant.llm_provider_model = custom_provider_model
        assistant.save()
        return
    except LlmProviderModel.DoesNotExist:
        pass

    new_custom_provider_model = LlmProviderModel.objects.create(
        team=assistant.team,
        type=assistant.llm_provider.type,
        name=assistant.llm_model,
    )
    assistant.llm_provider_model = new_custom_provider_model
    assistant.save()

def _handle_llm_experiment(LlmProviderModel, experiment):
    try:
        global_provider_model = LlmProviderModel.objects.get(
            team__isnull=True,
            type=experiment.llm_provider.type,
            name=experiment.llm,
            max_token_limit=experiment.max_token_limit
        )
        experiment.llm_provider_model = global_provider_model
        experiment.save()
        return
    except LlmProviderModel.DoesNotExist:
        pass

    try:
        custom_provider_model = LlmProviderModel.objects.get(
            team=experiment.team,
            type=experiment.llm_provider.type,
            name=experiment.llm,
            max_token_limit=experiment.max_token_limit
        )
        experiment.llm_provider_model = custom_provider_model
        experiment.save()
        return
    except LlmProviderModel.DoesNotExist:
        pass

    new_custom_provider_model = LlmProviderModel.objects.create(
        team=experiment.team,
        type=experiment.llm_provider.type,
        name=experiment.llm,
        max_token_limit=experiment.max_token_limit,
    )
    experiment.llm_provider_model = new_custom_provider_model
    experiment.save()

def _create_custom_llm_provider_models(apps, schema_editor):
    LlmProvider = apps.get_model("service_providers", "LlmProvider")
    LlmProviderModel = apps.get_model("service_providers", "LlmProviderModel")
    Experiment = apps.get_model("experiments", "Experiment")
    Analysis = apps.get_model("analysis", "Analysis")
    Node = apps.get_model("pipelines", "Node")

    for analysis in Analysis.objects.select_related("llm_provider").all():
        _handle_analysis(LlmProviderModel, analysis)

    for node in Node.objects.filter(Q(type="LLMResponseWithPrompt") | Q(type="LLMResponse") | Q(type="RouterNode")).all():
        _handle_pipeline_node(LlmProvider, LlmProviderModel, node)

    for experiment in Experiment.objects.select_related("llm_provider").all():
        if experiment.llm_provider is None and experiment.assistant:
            _handle_assistant(LlmProviderModel, experiment.assistant)
            continue

        if experiment.llm_provider is None and experiment.pipeline:
            # _handle_pipeline(LlmProviderModel, pipeline)
            continue

        _handle_llm_experiment(LlmProviderModel, experiment)



def _delete_all_llm_provider_models(apps, schema_editor):
    LlmProviderModel = apps.get_model("service_providers", "LlmProviderModel")
    LlmProviderModel.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('service_providers', '0018_llmprovidermodel'),
    ]

    operations = [migrations.RunPython(_create_llm_provider_models, reverse_code=_delete_all_llm_provider_models)
    ]

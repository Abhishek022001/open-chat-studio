from typing import TypedDict

from django.core.exceptions import FieldDoesNotExist, ValidationError

from apps.custom_actions.models import CustomActionOperation, make_model_id


class CustomActionOperationInfo(TypedDict):
    custom_action_id: int
    operation_id: str


def get_custom_action_operation_choices(team):
    return [
        (make_model_id(None, action["id"], operation), f"{action['name']}: {operation}")
        for action in team.customaction_set.all().values("id", "name", "operation_ids")
        for operation in action["operation_ids"]
    ]


def initialize_form_for_custom_actions(team, form):
    form.fields["custom_action_operations"].choices = get_custom_action_operation_choices(team)
    if form.instance and form.instance.id:
        form.initial["custom_action_operations"] = [
            op.get_model_id(with_holder=False) for op in form.instance.custom_action_operations.all()
        ]


def clean_custom_action_operations(form):
    operations = form.cleaned_data["custom_action_operations"]
    parsed_operations = []
    for op in operations:
        action_id, operation_id = op.split(":", 1)
        try:
            action_id = int(action_id)
        except ValueError:
            raise ValidationError("Invalid custom action operation")
        parsed_operations.append({"custom_action_id": action_id, "operation_id": operation_id})
    return parsed_operations


def set_custom_actions(holder, custom_action_infos: list[CustomActionOperationInfo]):
    """
    Set the custom actions for the holder.

    Args:
        holder: The holder model instance, an Experiment or an OpenAiAssistant.
        custom_action_infos: A list of dictionaries containing the custom action information.
    """
    if not hasattr(holder, "custom_action_operations"):
        raise FieldDoesNotExist(f"{holder.__class__.__name__} does not have a custom_action_operations field")

    def _clear_query_cache():
        holder.refresh_from_db(fields=["custom_actions", "custom_action_operations"])

    model_field = holder._meta.get_field("custom_action_operations")
    holder_kwarg = model_field.remote_field.name
    holder_kwargs = {holder_kwarg: holder}
    if not custom_action_infos:
        CustomActionOperation.objects.filter(**holder_kwargs).delete()
        _clear_query_cache()
        return

    action_ops_by_id = {action_op.get_model_id(): action_op for action_op in holder.custom_action_operations.all()}
    for info in custom_action_infos:
        op_id = make_model_id(holder.id, **info)
        op = action_ops_by_id.pop(op_id, None)
        if not op:
            CustomActionOperation.objects.create(**holder_kwargs, **info)

    if action_ops_by_id:
        old_ids = [old.id for old in action_ops_by_id.values()]
        CustomActionOperation.objects.filter(id__in=old_ids).delete()

    _clear_query_cache()

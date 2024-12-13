from django.conf import settings
from django.utils.safestring import mark_safe
from django_tables2 import columns, tables

from apps.assistants.models import OpenAiAssistant
from apps.generics import actions


class OpenAiAssistantTable(tables.Table):
    name = columns.Column(
        linkify=False,
        orderable=True,
    )
    actions = actions.ActionsColumn(
        actions=[
            actions.edit_action(
                "assistants:edit",
                required_permissions=["assistants.change_openaiassistant"],
            ),
            actions.AjaxAction(
                "assistants:sync",
                title="Update from OpenAI",
                icon_class="fa-solid fa-rotate",
                required_permissions=["assistants.change_openaiassistant"],
            ),
            actions.AjaxAction(
                "assistants:delete_local",
                title="Archive",
                icon_class="fa-solid fa-trash",
                required_permissions=["assistants.delete_openaiassistant"],
                confirm_message="This will only not delete the assistant from OpenAI.",
                hx_method="delete",
            ),
            actions.AjaxAction(
                "assistants:delete",
                title="Delete from OpenAI",
                icon_class="fa-solid fa-trash-arrow-up",
                required_permissions=["assistants.delete_openaiassistant"],
                confirm_message="This will also delete the assistant from OpenAI. Are you sure?",
                hx_method="delete",
            ),
        ]
    )

    def render_name(self, record):
        return mark_safe(f'<a href="{record.get_absolute_url()}" class="link">{record.name}</a>')

    class Meta:
        model = OpenAiAssistant
        fields = ("name", "assistant_id")
        row_attrs = settings.DJANGO_TABLES2_ROW_ATTRS
        orderable = False
        empty_text = "No assistants found."

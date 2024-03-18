from django.conf import settings
from django_tables2 import columns, tables

from apps.generics import actions

from .models import Tag


class TagTable(tables.Table):
    actions = columns.TemplateColumn(
        template_name="generic/crud_actions_column.html",
        extra_context={
            "actions": [
                actions.edit_action(url_name="annotations:tag_edit"),
                actions.delete_action(url_name="annotations:tag_delete"),
            ]
        },
    )

    class Meta:
        model = Tag
        fields = ("name",)
        row_attrs = settings.DJANGO_TABLES2_ROW_ATTRS
        orderable = False
        empty_text = "No tags found."

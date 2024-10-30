from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView
from django_tables2 import SingleTableView

from apps.custom_actions.forms import CustomActionForm
from apps.custom_actions.models import CustomAction
from apps.custom_actions.tables import CustomActionTable
from apps.teams.mixins import LoginAndTeamRequiredMixin


class CustomActionHome(LoginAndTeamRequiredMixin, TemplateView):
    template_name = "generic/object_home.html"

    def get_context_data(self, team_slug: str, **kwargs):
        return {
            "active_tab": "custom_actions",
            "title": "Custom Actions",
            # "info_link": settings.DOCUMENTATION_LINKS["consent"],
            "new_object_url": reverse("custom_actions:new", args=[team_slug]),
            "table_url": reverse("custom_actions:table", args=[team_slug]),
        }


class CustomActionTableView(SingleTableView):
    model = CustomAction
    paginate_by = 25
    table_class = CustomActionTable
    template_name = "table/single_table.html"

    def get_queryset(self):
        return CustomAction.objects.filter(team=self.request.team)


class CreateCustomAction(CreateView):
    model = CustomAction
    form_class = CustomActionForm
    template_name = "generic/object_form.html"
    extra_context = {
        "title": "Create Custom Action",
        "button_text": "Create",
        "active_tab": "custom_actions",
    }

    def get_success_url(self):
        return reverse("single_team:manage_team", args=[self.request.team.slug])

    def form_valid(self, form):
        form.instance.team = self.request.team
        return super().form_valid(form)


class EditCustomAction(UpdateView):
    model = CustomAction
    form_class = CustomActionForm
    template_name = "generic/object_form.html"
    extra_context = {
        "title": "Update Custom Action",
        "button_text": "Update",
        "active_tab": "custom_actions",
    }

    def get_queryset(self):
        return CustomAction.objects.filter(team=self.request.team)

    def get_success_url(self):
        return reverse("single_team:manage_team", args=[self.request.team.slug])


class DeleteCustomAction(LoginAndTeamRequiredMixin, View):
    def delete(self, request, team_slug: str, pk: int):
        consent_form = get_object_or_404(CustomAction, id=pk, team=request.team)
        consent_form.delete()
        messages.success(request, "Custom Action Deleted")
        return HttpResponse()

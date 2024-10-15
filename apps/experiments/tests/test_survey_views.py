import pytest
from django.test import RequestFactory
from django.urls import reverse

from apps.experiments.models import Survey
from apps.experiments.views.survey import SurveyTableView
from apps.utils.factories.experiment import ExperimentFactory
from apps.utils.factories.team import TeamWithUsersFactory


class TestSurveyTableView:
    def test_get_queryset(self, experiment):
        assert experiment.pre_survey is not None
        experiment.create_new_version()
        assert Survey.objects.count() == 2

        request = RequestFactory().get(reverse("experiments:survey_table", args=[experiment.team.slug]))
        request.team = experiment.team
        view = SurveyTableView()
        view.request = request
        assert list(view.get_queryset().all()) == [experiment.pre_survey]


@pytest.mark.django_db()
def test_delete(client):
    team = TeamWithUsersFactory()
    user = team.members.first()
    experiment = ExperimentFactory(team=team)
    client.force_login(user)
    survey = experiment.pre_survey
    url = reverse("experiments:survey_delete", args=[experiment.team.slug, survey.id])
    response = client.delete(url)
    assert response.status_code == 200
    survey.refresh_from_db()
    assert survey.is_archived is True

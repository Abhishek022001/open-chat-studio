from django.urls import include, path
from rest_framework import routers

from . import openai, views

app_name = "api"

router = routers.SimpleRouter()
router.register(r"experiments", views.ExperimentViewSet, basename="experiment")
router.register(r"sessions", views.ExperimentSessionViewSet, basename="session")

urlpatterns = [
    path("participants/", views.update_participant_data, name="update-participant-data"),
    path("openai/<uuid:experiment_id>/chat/completions", openai.chat_completions, name="openai-chat-completions"),
    path("files/<int:pk>/content", views.file_content_view, name="file-content"),
    path("", include(router.urls)),
]

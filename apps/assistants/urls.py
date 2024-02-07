from django.urls import path

from apps.assistants import views
from apps.generics.urls import make_crud_urls

app_name = "assistants"

urlpatterns = make_crud_urls(views, "OpenAiAssistant", "") + [
    path("import/", views.ImportAssistant.as_view(), name="import"),
    path("<int:pk>/delete_local/", views.LocalDeleteOpenAiAssistant.as_view(), name="delete_local"),
    path("<int:pk>/sync/", views.SyncOpenAiAssistant.as_view(), name="sync"),
]

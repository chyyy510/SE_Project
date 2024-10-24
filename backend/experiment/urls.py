from django.urls import path
from .views import ExperimentList

urlpatterns = [
    path("", ExperimentList.as_view(), name="experiment-list"),
]

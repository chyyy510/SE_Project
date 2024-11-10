from django.urls import path
from experiment.views import ExperimentList, ExperimentCreate

urlpatterns = [
    path("", ExperimentList.as_view(), name="experiment-list"),
    path("create/", ExperimentCreate.as_view(), name="experiment-create"),
]

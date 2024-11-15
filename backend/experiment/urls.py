from django.urls import path
from experiment.views import ExperimentList, ExperimentCreate, ExperimentSearch

urlpatterns = [
    path("", ExperimentList.as_view(), name="experiment-list"),
    path("create/", ExperimentCreate.as_view(), name="experiment-create"),
    path("search/", ExperimentSearch.as_view(), name="experiment-search"),
]

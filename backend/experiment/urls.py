from django.urls import path
from experiment.views import (
    ExperimentList,
    ExperimentDetail,
    ExperimentCreate,
    ExperimentSearch,
)

urlpatterns = [
    path("", ExperimentList.as_view(), name="experiment-list"),
    path("<int:pk>/", ExperimentDetail.as_view(), name="experiment-detail"),
    path("create/", ExperimentCreate.as_view(), name="experiment-create"),
    path("search/", ExperimentSearch.as_view(), name="experiment-search"),
]

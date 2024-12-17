from django.urls import path
from experiment.views import (
    ExperimentList,
    ExperimentDetail,
    ExperimentCreate,
    ExperimentSearch,
    ExperimentSearchInCreated,
    ExperimentClose,
    ExperimentEdit,
)

urlpatterns = [
    path("", ExperimentList.as_view(), name="experiment-list"),
    path("<int:pk>/", ExperimentDetail.as_view(), name="experiment-detail"),
    path("create/", ExperimentCreate.as_view(), name="experiment-create"),
    path("search/", ExperimentSearch.as_view(), name="experiment-search"),
    path(
        "create/search/",
        ExperimentSearchInCreated.as_view(),
        name="experiment-create-search",
    ),
    path("close/", ExperimentClose.as_view(), name="experiment-close"),
    path("edit/", ExperimentEdit.as_view(), name="experiment-edit"),
]

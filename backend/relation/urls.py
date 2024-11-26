from django.urls import path
from relation.views import (
    EngagementCreate,
    EngagementList,
    ExperimentEngagedList,
    ExperimentCreatedList,
)

urlpatterns = [
    path("engagements/create/", EngagementCreate.as_view(), name="engagement-create"),
    path("engagements/list/", EngagementList.as_view(), name="engagements-list"),
    path(
        "experiments-engaged/list/",
        ExperimentEngagedList.as_view(),
        name="exp-engaged-list",
    ),
    path(
        "experiments-created/list/",
        ExperimentCreatedList.as_view(),
        name="exp-created-list",
    ),
]

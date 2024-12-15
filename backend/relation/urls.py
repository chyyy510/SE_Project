from django.urls import path
from relation.views import (
    EngagementCreate,
    ExperimentSearchInEngaged,
    VolunteerQualify,
)

urlpatterns = [
    path("engage/", EngagementCreate.as_view(), name="experiment-engage"),
    path(
        "engage/search/",
        ExperimentSearchInEngaged.as_view(),
        name="experiment-engage-search",
    ),
    path(
        "qualify/volunteers/",
        VolunteerQualify.as_view(),
        name="qualify-volunteer",
    ),
]

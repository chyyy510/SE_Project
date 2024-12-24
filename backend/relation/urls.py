from django.urls import path
from relation.views import (
    EngagementCreate,
    EngagementCancel,
    ExperimentSearchInEngaged,
    VolunteerQualify,
    VolunteerList,
    TagsView,
)

urlpatterns = [
    path("engage/", EngagementCreate.as_view(), name="experiment-engage"),
    path(
        "engage/search/",
        ExperimentSearchInEngaged.as_view(),
        name="experiment-engage-search",
    ),
    path("engage/cancel/", EngagementCancel.as_view(), name="experiment-engage-cancel"),
    path(
        "qualify/volunteers/",
        VolunteerQualify.as_view(),
        name="qualify-volunteer",
    ),
    path("volunteers/list/", VolunteerList.as_view(), name="volunteer-list"),
    path(
        "tags/",
        TagsView.as_view(),
        name="tags",
    ),
]

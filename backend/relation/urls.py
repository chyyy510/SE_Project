from django.urls import path
from relation.views import EngagementCreate, EngagementList, CreationList

urlpatterns = [
    path("engagements/create/", EngagementCreate.as_view(), name="engagement-create"),
    path("engagements/list/", EngagementList.as_view(), name="engagement-list"),
    path("creation/list/", CreationList.as_view(), name="creation-list"),
]

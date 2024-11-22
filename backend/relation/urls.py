from django.urls import path
from relation.views import EngagementCreate, EngagementList

urlpatterns = [
    path("engagements/create/", EngagementCreate.as_view(), name="engagement-create"),
    path("engagements/list/", EngagementList.as_view(), name="engagement-list"),
]

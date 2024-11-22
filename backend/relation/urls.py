from django.urls import path
from relation.views import EngagementCreate

urlpatterns = [
    path("engagement/create/", EngagementCreate.as_view(), name="engagement-create"),
]

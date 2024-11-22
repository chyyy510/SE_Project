from rest_framework import status
from rest_framework.response import Response
from relation.models import Engagement
from experiment.models import Experiment
from relation.serializers import EngagementSerializer

from django.contrib.auth.models import AnonymousUser

from rest_framework import generics


# Create your views here.


class EngagementCreate(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        if isinstance(request.user, AnonymousUser):
            return Response(
                {"detail": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        eid = request.data.get("experiment")

        try:
            experiment = Experiment.objects.get(id=eid)
        except:
            return Response(
                {"message": "The experiment doesn't exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # 也得检测这个用户是否参与过该实验

        engagement_exist = Engagement.objects.filter(
            user=user, experiment=experiment
        ).exists()

        if engagement_exist:
            return Response(
                {"message": "User has engaged in this experiment."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        engagement = Engagement(
            user=user, experiment=experiment, status="user-qualification"
        )

        engagement.save()

        serializer = EngagementSerializer(engagement)

        return Response(serializer.data)

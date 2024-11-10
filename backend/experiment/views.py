from rest_framework import status
from rest_framework.response import Response
from experiment.models import Experiment
from experiment.serializers import ExperimentSerializer, ExperimentCreateSerializer

from rest_framework import generics
from django.utils import timezone

# Create your views here.


class ExperimentList(generics.ListAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer


class ExperimentCreate(generics.GenericAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentCreateSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        title = request.data.get("title")
        description = request.data.get("description")
        person_wanted = request.data.get("person_wanted")
        money_per_person = request.data.get("money_per_person")
        # ?creator=user

        print("{}", user)

        experiment = Experiment(
            title=title,
            description=description,
            status="open",
            creator=user,
            person_wanted=person_wanted,
            person_already=0,
            money_per_person=money_per_person,
            money_paid=0,  # TODO:
            money_left=0,  # TODO:
            time_created=timezone.now(),
            time_modified=timezone.now(),
        )

        experiment.save()

        serializer = ExperimentCreateSerializer(experiment)

        return Response(serializer.data)

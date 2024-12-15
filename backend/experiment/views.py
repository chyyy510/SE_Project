from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import AnonymousUser
from experiment.models import Experiment
from experiment.serializers import ExperimentSerializer, ExperimentCreateSerializer

from rest_framework import generics
from django.utils import timezone

# Create your views here.


class ExperimentPagination(PageNumberPagination):
    page_size = 10  # 每页显示的条目数
    page_size_query_param = "page_size"  # 允许通过查询参数调整每页条目数
    max_page_size = 100  # 限制最大每页条目数


class ExperimentList(generics.ListAPIView):
    queryset = Experiment.objects.all().order_by("id")
    serializer_class = ExperimentSerializer
    pagination_class = ExperimentPagination


class ExperimentDetail(generics.RetrieveAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer

    def get(self, request, *args, **kwargs):
        try:
            response = super().get(request, *args, **kwargs)
            response.data["message"] = (
                "Find the experiment successfully. 成功找到该实验。"
            )
        except Exception:
            return Response(
                {"detail": "Experiment doesn't exist. 该实验不存在。"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return response


class ExperimentCreate(generics.GenericAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentCreateSerializer

    def post(self, request, *args, **kwargs):

        if isinstance(request.user, AnonymousUser):
            return Response(
                {"detail": "Authentication required. 该功能需要先登录。"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user = request.user

        title = request.data.get("title")
        description = request.data.get("description")
        person_wanted = request.data.get("person_wanted")
        money_per_person = request.data.get("money_per_person")
        activity_time = request.data.get("activity_time", "2024-01-01")
        activity_location = request.data.get("activity_location", "北京大学")
        # ?creator=user

        # print("{}", user)
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
            activity_time=activity_time,
            activity_location=activity_location,
        )

        try:
            experiment.save()
        except Exception:
            return Response(
                {"detail": "Format error. 有内容不符合格式。"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ExperimentSerializer(experiment)

        return Response(serializer.data)


class ExperimentSearch(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        title = request.GET.get("title", "")
        description = request.GET.get("description", "")

        orderby = request.GET.get("orderby", "id")

        if hasattr(Experiment, orderby) == False:
            orderby = "id"

        sort = request.GET.get("sort", "asc")

        if sort == "desc":
            orderby = f"-{orderby}"  # 使用负号表示降序排序

        experiments = Experiment.objects.filter(
            title__contains=title, description__contains=description
        ).order_by(orderby)

        # 分页处理
        paginator = ExperimentPagination()
        paginated_experiments = paginator.paginate_queryset(experiments, request)

        serializer = ExperimentSerializer(paginated_experiments, many=True)
        return paginator.get_paginated_response(serializer.data)


class ExperimentSearchInCreated(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            return Response(
                {"detail": "Authentication required. 该功能需要先登录。"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user = request.user

        title = request.GET.get("title", "")
        description = request.GET.get("description", "")

        orderby = request.GET.get("orderby", "id")

        if hasattr(Experiment, orderby) == False:
            orderby = "id"

        sort = request.GET.get("sort", "asc")

        if sort == "desc":
            orderby = f"-{orderby}"  # 使用负号表示降序排序

        experiments = Experiment.objects.filter(
            creator=user, title__contains=title, description__contains=description
        ).order_by(orderby)

        # 分页处理
        paginator = ExperimentPagination()
        paginated_experiments = paginator.paginate_queryset(experiments, request)

        serializer = ExperimentSerializer(paginated_experiments, many=True)
        return paginator.get_paginated_response(serializer.data)

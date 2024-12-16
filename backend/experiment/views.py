from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from appuser.models import User
from experiment.models import Experiment
from experiment.serializers import ExperimentSerializer, ExperimentCreateSerializer
from relation.models import TagsExps

from rest_framework import generics
from django.utils import timezone

from utils.log_print import log_print

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
            response = Response(
                {"detail": "Experiment doesn't exist. 该实验不存在。"},
                status=status.HTTP_404_NOT_FOUND,
            )

        relationship = ""
        user = request.user
        creator_id = response.data["creator"]
        try:
            creator = User.objects.get(id=creator_id)
        except Exception:
            return Response(
                {"detail": "The experiment creator doesn't exist. 实验创建者不存在。"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response.data["creator"] = creator.username

        if isinstance(user, AnonymousUser):
            relationship = "unauthorized"
        else:

            if creator == user:
                relationship = "creator"
            else:
                relationship = "applicant"

        response.data["relationship"] = relationship

        return response


class ExperimentCreate(generics.GenericAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentCreateSerializer

    def post(self, request, *args, **kwargs):
        log_print(request.headers)
        log_print(request.data)
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

        tags = request.data.get("tags", 0)

        def int_to_bitset(n):
            bitset = set()
            position = 1
            while n > 0:
                if n & 1:
                    bitset.add(position)
                n >>= 1
                position += 1
            return bitset

        # ?creator=user

        # debug_print("{}", user)
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
            for tag_id in int_to_bitset(tags):
                TagsExps(tags=tag_id, experiment=experiment.id).save()
        except Exception:
            return Response(
                {"detail": "Format error. 有内容不符合格式。"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ExperimentSerializer(experiment)

        return Response(serializer.data)


class ExperimentSearch(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        keyword = request.GET.get("keyword", "")

        orderby = request.GET.get("orderby", "id")

        if hasattr(Experiment, orderby) == False:
            orderby = "id"

        sort = request.GET.get("sort", "asc")

        if sort == "desc":
            orderby = f"-{orderby}"  # 使用负号表示降序排序

        experiments = Experiment.objects.filter(
            Q(title__contains=keyword) | Q(description__contains=keyword)
        ).order_by(orderby)

        # 分页处理
        paginator = ExperimentPagination()
        paginated_experiments = paginator.paginate_queryset(experiments, request)

        serializer = ExperimentSerializer(paginated_experiments, many=True)
        return paginator.get_paginated_response(serializer.data)


class ExperimentAdvancedSearch(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        keyword = request.GET.get("keyword", "")

        orderby = request.GET.get("orderby", "id")

        if not hasattr(Experiment, orderby):
            orderby = "id"

        sort = request.GET.get("sort", "asc")

        if sort == "desc":
            orderby = f"-{orderby}"  # 使用负号表示降序排序

        experiments = Experiment.objects.filter(
            Q(title__contains=keyword) | Q(description__contains=keyword)
        ).order_by(orderby)

        # 分页处理
        paginator = ExperimentPagination()
        paginated_experiments = paginator.paginate_queryset(experiments, request)

        serializer = ExperimentSerializer(paginated_experiments, many=True)
        return paginator.get_paginated_response(serializer.data)


class ExperimentAdvancedSearch(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        title = request.GET.get("title", "")
        description = request.GET.get("description", "")

        orderby = request.GET.get("orderby", "id")

        if not hasattr(Experiment, orderby):
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

        keyword = request.GET.get("keyword", "")

        orderby = request.GET.get("orderby", "id")

        if hasattr(Experiment, orderby) == False:
            orderby = "id"

        sort = request.GET.get("sort", "asc")

        if sort == "desc":
            orderby = f"-{orderby}"  # 使用负号表示降序排序

        experiments = Experiment.objects.filter(
            Q(creator=user)
            & (Q(title__contains=keyword) | Q(description__contains=keyword))
        ).order_by(orderby)

        # 分页处理
        paginator = ExperimentPagination()
        paginated_experiments = paginator.paginate_queryset(experiments, request)

        serializer = ExperimentSerializer(paginated_experiments, many=True)
        return paginator.get_paginated_response(serializer.data)


class ExperimentAdvancedSearchInCreated(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            return Response(
                {"detail": "Authentication required. 该功能需要先登录。"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user = request.user

        keyword = request.GET.get("keyword", "")

        orderby = request.GET.get("orderby", "id")

        if not hasattr(Experiment, orderby):
            orderby = "id"

        sort = request.GET.get("sort", "asc")

        if sort == "desc":
            orderby = f"-{orderby}"  # 使用负号表示降序排序

        experiments = Experiment.objects.filter(
            Q(creator=user)
            & (Q(title__contains=keyword) | Q(description__contains=keyword))
        ).order_by(orderby)

        # 分页处理
        paginator = ExperimentPagination()
        paginated_experiments = paginator.paginate_queryset(experiments, request)

        serializer = ExperimentSerializer(paginated_experiments, many=True)
        return paginator.get_paginated_response(serializer.data)


class ExperimentAdvancedSearchInCreated(generics.GenericAPIView):
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

        if not hasattr(Experiment, orderby):
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


class ExperimentClose(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            return Response(
                {"detail": "Authentication required. 该功能需要先登录。"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user = request.user

        eid = request.data.get("experiment")
        try:
            experiment = Experiment.objects.get(id=eid)
        except Exception:
            return Response(
                {"detail": "The experiment doesn't exist. 该实验不存在。"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if experiment.creator != user:
            return Response(
                {"detail": "Not accessible. 当前用户无权操作"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if experiment.status == "close":
            return Response(
                {"detail": "The experiment had been closed. 该实验早已被关闭。"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        experiment.status = "close"
        experiment.save()
        return Response(
            {"message": "Successfully close the experiment. 成功关闭实验。"},
            status=status.HTTP_200_OK,
        )


class ExperimentEdit(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            return Response(
                {"detail": "Authentication required. 该功能需要先登录。"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user = request.user
        id = request.data.get("id")
        if id is None:
            return Response(
                {"detail": "Exp id please. 请提供实验 id。"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if Experiment.objects.get(id=id).creator != user:
            return Response(
                {
                    "detail": "You are not the creator of this experiment. 您不是此实验的创建者。"
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        attri = dict()

        if (title := request.data.get("title")) is not None:
            attri["title"] = title
        if (description := request.data.get("description")) is not None:
            attri["description"] = description
        if (person_wanted := request.data.get("person_wanted")) is not None:
            attri["person_wanted"] = person_wanted
        if (money_per_person := request.data.get("money_per_person")) is not None:
            attri["money_per_person"] = money_per_person
        if (activity_time := request.data.get("activity_time")) is not None:
            attri["activity_time"] = activity_time
        if (activity_location := request.data.get("activity_location")) is not None:
            attri["activity_location"] = activity_location

        try:
            Experiment.objects.get(id=id).update(**attri)
            return Response(
                {"detail": "Experiment info edited successfully. 实验信息更新成功。"}
            )

        except Exception:
            return Response(
                {"detail": "Format error. 有内容不符合格式。"},
                status=status.HTTP_400_BAD_REQUEST,
            )

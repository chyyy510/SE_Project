from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from relation.models import Engagement, Tags
from experiment.models import Experiment
from experiment.views import ExperimentPagination
from relation.serializers import EngagementSerializer, TagsSerializer
from experiment.serializers import ExperimentSerializer

from django.contrib.auth.models import AnonymousUser

from rest_framework import generics


# Create your views here.


class EngagementPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class EngagementCreate(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        if isinstance(request.user, AnonymousUser):
            return Response(
                {"detail": "Authentication required. 该功能需要先登录。"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        eid = request.data.get("experiment")

        try:
            experiment = Experiment.objects.get(id=eid)
        except:
            return Response(
                {"detail": "The experiment doesn't exist. 该实验不存在。"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # 也得检测这个用户是否参与过该实验

        engagement_exist = Engagement.objects.filter(
            user=user, experiment=experiment
        ).exists()

        if engagement_exist:
            return Response(
                {
                    "detail": "User has engaged in this experiment. 用户已经参与过该实验。"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        engagement = Engagement(
            user=user, experiment=experiment, status="user-qualification"
        )

        engagement.save()

        serializer = EngagementSerializer(engagement)

        return Response(serializer.data)


class ExperimentSearchInEngaged(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            return Response(
                {"detail": "Authentication required. 该功能需要先登录。"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        user = request.user
        engagements = Engagement.objects.filter(user=user).order_by("id")
        # experiments_id = engagements.values("experiment")
        experiment_ids = engagements.values_list("experiment_id", flat=True).distinct()

        # 根据 experiment_id 查询对应的 Experiment 信息
        experiments = Experiment.objects.filter(id__in=experiment_ids)

        title = request.GET.get("title", "")
        description = request.GET.get("description", "")

        orderby = request.GET.get("orderby", "id")

        if hasattr(Experiment, orderby) == False:
            orderby = "id"

        sort = request.GET.get("sort", "asc")

        if sort == "desc":
            orderby = f"-{orderby}"  # 使用负号表示降序排序

        experiments = experiments.order_by(orderby)

        # 分页处理
        paginator = ExperimentPagination()
        paginated_experiments = paginator.paginate_queryset(experiments, request)

        serializer = ExperimentSerializer(paginated_experiments, many=True)
        return paginator.get_paginated_response(serializer.data)


class VolunteerQualify(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            return Response(
                {"detail": "Authentication required. 该功能需要先登录。"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        user = request.user
        experiment_id = request.data.get("experiment_id")
        experiment = Experiment.objects.get(id=experiment_id)

        if experiment.creator != user:
            return Response(
                {
                    "detail": "The experiment doesn't belong to the user. 该实验非当前用户所创建。"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        volunteer_id = request.data.get("volunteer_id")
        try:
            engagement = Engagement.objects.get(
                user=volunteer_id, experiment=experiment_id
            )
        except Engagement.DoesNotExist:
            return Response(
                {
                    "detail": "The volunteer didn't engage in the experiment. 该志愿者并未参与此实验。"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Engagement.MultipleObjectsReturned:
            return Response(
                {
                    "detail": "Same volunteer engaged in the experiment multiple times. 该志愿者重复参与了此实验。"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        qualification = request.data.get("qualification")

        # 检查是否在三个选项里，以及转换方向
        in_flag = False

        for tp in Engagement.status_choice:
            if tp[0] == qualification:
                in_flag = True
                break

        if in_flag == False:  # 不在
            return Response(
                {"detail": "Status error. 没有这一状态。"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 在,检查转换方向#TODO:换个更好的写法？
        match (engagement.status, qualification):
            case ("to-qualify-user", "to-check-result") | ("to-check-result", "finish"):
                engagement.status = qualification
                engagement.save()

                return Response(
                    {
                        "message": "Volunteer status changed successfully. 成功转换志愿者审核状态。"
                    },
                    status=status.HTTP_200_OK,
                )
            case _:
                return Response(
                    {"detail": "Status transition error. 不能这样转换状态。"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        # if engagement.status == "to-qualify-user":
        #     if qualification != "to-check-result":
        #         return Response(
        #             {"detail": "Status transition error. 不能这样转换状态。"},
        #             status=status.HTTP_400_BAD_REQUEST,
        #         )

        # if engagement.status == "to-check-result":
        #     if qualification != "finish":
        #         return Response(
        #             {"detail": "Status transition error. 不能这样转换状态。"},
        #             status=status.HTTP_400_BAD_REQUEST,
        #         )

        # if engagement.status == "finish":
        #     return Response(
        #         {"detail": "Status transition error. 不能这样转换状态。"},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )

        # engagement.status = qualification
        # engagement.save()

        # return Response(
        #     {
        #         "message": "Volunteer status changed successfully. 成功转换志愿者审核状态。"
        #     },
        #     status=status.HTTP_200_OK,
        # )


class TagsView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        tags = Tags.objects.all()
        serializer = TagsSerializer(tags, many=True)
        return Response(serializer.data)  # 返回 JSON 数据

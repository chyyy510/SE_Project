from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from appuser.models import User, UserProfile
from relation.models import Engagement, Tags, TagsExps
from experiment.models import Experiment
from appuser.views import UserUsernamePagination
from experiment.views import ExperimentPagination
from appuser.serializers import UserUsernameSerializer, UsernameStatusSerializer
from relation.serializers import (
    EngagementSerializer,
    TagsSerializer,
    VolunteerListSerializer,
)
from experiment.serializers import ExperimentSerializer, ExperimentDetailSerializer

from django.contrib.auth.models import AnonymousUser

from rest_framework import generics

from utils.log_print import log_print
from utils.get_set_bits_positions import get_set_bits_positions

# Create your views here.


class EngagementPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class EngagementCreate(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        log_print(request.headers, request.data)
        user = request.user
        if isinstance(request.user, AnonymousUser):
            return Response(
                {"detail": "Authentication required. 该功能需要先登录。"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        eid = request.data.get("experiment", 0)

        try:
            experiment = Experiment.objects.get(id=eid)
        except:
            return Response(
                {"detail": "The experiment doesn't exist. 该实验不存在。"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if experiment.status == "close":
            return Response(
                {"detail": "This experiment had been closed. 该实验已关闭。"},
                status=status.HTTP_400_BAD_REQUEST,
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
            user=user, experiment=experiment, status="to-qualify-user"
        )

        experiment.person_already = experiment.person_already + 1
        try:
            experiment.save()
            engagement.save()
        except Exception:
            return Response(
                {"detail": "Save to database error. 保存到数据库失败。"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = EngagementSerializer(engagement)

        return Response(serializer.data)


class EngagementCancel(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        log_print(request.headers, request.data)

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

        if experiment.status == "close":
            return Response(
                {"detail": "This experiment had been closed. 该实验已关闭。"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            engagement = Engagement.objects.get(experiment=experiment, user=user)
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
        except Exception as e:
            return Response(
                {
                    "detail": "An unexpected error occurred. 出现了一个意外的错误。{}".format(
                        str(e)
                    )
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if engagement.status == "to-check-result":
            return Response(
                {"detail": "On going, not allowed to cancel. 进行中，不允许取消。"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif engagement.status == "finish":
            return Response(
                {"detail": "Finish, not allowed to cancel. 已完成，不允许取消。"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 可以取消，处理相关影响。TODO:

        engagement.delete()
        experiment.person_already -= 1
        experiment.save()
        serializer = ExperimentDetailSerializer(experiment)
        response = Response(serializer.data)
        response["message"] = "Successfully cancel the engagement. 成功取消参与。"
        return response


class ExperimentSearchInEngaged(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        log_print(request.headers, request.data)
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
        # experiments = Experiment.objects.filter(id__in=experiment_ids)
        tags = request.GET.get("tags", 0)
        keyword = request.GET.get("keyword", "")

        orderby = request.GET.get("orderby", "id")

        if hasattr(Experiment, orderby) == False:
            orderby = "id"

        sort = request.GET.get("sort", "asc")

        if sort == "desc":
            orderby = f"-{orderby}"  # 使用负号表示降序排序
        # 先筛符合tag的

        pre_set = set(Experiment.objects.values_list("id", flat=True))

        pos = get_set_bits_positions(int(tags))

        for tag in pos:
            tagsexps = TagsExps.objects.filter(tags=tag).select_related("experiment")
            now_set = {instance.experiment.id for instance in tagsexps}
            log_print(type(pre_set), type(now_set))
            pre_set = pre_set.intersection(now_set)
        log_print(pre_set)

        final_set = Experiment.objects.filter(
            Q(id__in=pre_set) & Q(id__in=experiment_ids)
        )
        experiments = final_set.filter(
            Q(title__contains=keyword) | Q(description__contains=keyword)
        ).order_by(orderby)

        # 分页处理
        paginator = ExperimentPagination()
        paginated_experiments = paginator.paginate_queryset(experiments, request)

        serializer = ExperimentDetailSerializer(paginated_experiments, many=True)
        return paginator.get_paginated_response(serializer.data)


class ExperimentAdvancedSearchInEngaged(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        log_print(request.headers, request.data)
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

        serializer = ExperimentDetailSerializer(paginated_experiments, many=True)
        return paginator.get_paginated_response(serializer.data)


class VolunteerQualify(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        log_print(request.headers, request.data)
        if isinstance(request.user, AnonymousUser):
            return Response(
                {"detail": "Authentication required. 该功能需要先登录。"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        log_print("here")
        user = request.user
        experiment_id = request.data.get("experiment", 0)
        if experiment_id == 0:
            log_print("exception")
            return Response(
                {"detail": "Experiment id needed. 需指明experiment id。"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        experiment = Experiment.objects.get(id=experiment_id)
        log_print("here")

        if experiment.creator != user:
            return Response(
                {
                    "detail": "The experiment doesn't belong to the user. 该实验非当前用户所创建。"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if experiment.status == "close":
            return Response(
                {"detail": "The experiment had been closed. 该实验已被关闭。"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        log_print("here")

        volunteer_username = request.data.get("volunteer")
        try:
            volunteer_id = User.objects.get(username=volunteer_username)
        except Exception:
            return Response(
                {"detail": "The volunteer doesn't exist. 该志愿者不存在。"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        log_print("here")
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
        except Exception as e:
            return Response(
                {
                    "detail": "An unexpected error occurred. 出现了一个意外的错误。{}".format(
                        str(e)
                    )
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        log_print(engagement.status)

        match engagement.status:
            case "to-qualify-user":
                engagement.status = "to-check-result"
                engagement.save()

                return Response(
                    {
                        "status": "to-check-result",
                        "message": "Volunteer status changed successfully. 成功转换志愿者审核状态。",
                    },
                    status=status.HTTP_200_OK,
                )
            case "to-check-result":
                engagement.status = "finish"

                try:
                    volunteer = User.objects.get(username=volunteer_id)
                except Exception:
                    return Response(
                        {"detail": "Volunteer doesn't exist. 志愿者不存在。"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                point = experiment.money_per_person  # * 100
                try:
                    profile = UserProfile.objects.get(user=volunteer)
                except Exception:
                    return Response(
                        {
                            "detail": "Volunteer profile doesn't exist. 志愿者主页不存在。"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                profile.point = profile.point + point
                experiment.money_left -= point

                try:
                    engagement.save()
                    profile.save()
                    experiment.save()
                except Exception:
                    return Response(
                        {"detail": "Save to database error. 保存到数据库失败。"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                return Response(
                    {
                        "status": "finish",
                        "message": "Volunteer status changed successfully and points paid. 成功转换志愿者审核状态并发放报酬。",
                    },
                    status=status.HTTP_200_OK,
                )
            case "finish":
                return Response(
                    {
                        "detail": "The volunteer has finished the experiment. 该志愿者已完成实验。"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            case _:
                return Response(
                    {"detail": "Status transition error. 不能这样转换状态。"},
                    status=status.HTTP_400_BAD_REQUEST,
                )


# eid-> all ,check create
class VolunteerList(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        log_print(request.headers, request.data)
        user = request.user
        if isinstance(request.user, AnonymousUser):
            return Response(
                {"detail": "Authentication required. 该功能需要先登录。"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        eid = request.GET.get("experiment")

        try:
            experiment = Experiment.objects.get(id=eid)
        except:
            return Response(
                {"detail": "The experiment doesn't exist. 该实验不存在。"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if experiment.creator != user:
            return Response(
                {
                    "detail": "No access to this experiment. 当前用户无权查看该实验志愿者列表。"
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # 找所有volunteer
        engagements = Engagement.objects.filter(experiment=experiment).order_by("id")

        paginator = UserUsernamePagination()

        paginated_engagements = paginator.paginate_queryset(engagements, request)
        serializer = VolunteerListSerializer(paginated_engagements, many=all)
        return paginator.get_paginated_response(serializer.data)


class TagsView(generics.GenericAPIView):
    queryset = Tags.objects.all().order_by("id")

    def get(self, request, *args, **kwargs):
        log_print(request.headers, request.data)
        serializer = TagsSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)  # 返回 JSON 数据

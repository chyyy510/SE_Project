from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from appuser.models import User
from experiment.models import Experiment
from relation.models import Engagement, Tags, TagsExps

from experiment.serializers import (
    ExperimentSerializer,
    ExperimentDetailSerializer,
    ExperimentCreateSerializer,
)
from relation.serializers import TagsSerializer

from rest_framework import generics
from django.utils import timezone

from utils.log_print import log_print
from utils.generate_path import GeneratePath
from utils.get_set_bits_positions import get_set_bits_positions

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

        eid = kwargs.get("pk")

        try:  # TODO:看情况再修改
            experiment = Experiment.objects.get(id=eid)

        except Exception:
            return Response(
                {"detail": "Experiment doesn't exist. 该实验不存在。"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ExperimentDetailSerializer(experiment)
        response = Response(serializer.data)

        # 获取对应标签并转为二进制
        tagsexps = TagsExps.objects.filter(experiment=experiment).order_by("id")
        tags_id = tagsexps.values_list("tags", flat=True)
        tags = Tags.objects.filter(id__in=tags_id).distinct()
        serializer_tag = TagsSerializer(tags, many=True)
        response.data["tags"] = serializer_tag.data

        relationship = ""
        user = request.user
        creator_name = response.data["creator"]
        try:
            creator = User.objects.get(username=creator_name)
        except Exception:
            return Response(
                {"detail": "The experiment creator doesn't exist. 实验创建者不存在。"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        avatar = creator.userprofile.avatar.url

        response.data["message"] = "Find the experiment successfully. 成功找到该实验。"
        response.data["avatar"] = avatar

        if isinstance(user, AnonymousUser):
            relationship = "unauthorized"

        else:

            if creator == user:
                relationship = "creator"
            else:
                # 判断是否已参加
                try:
                    engagement = Engagement.objects.get(
                        experiment=experiment, user=user
                    )
                except Engagement.DoesNotExist:
                    relationship = "passer-by"
                    response.data["relationship"] = relationship

                    return response

                except Engagement.MultipleObjectsReturned:
                    return Response(
                        {"detail": "Multiple engagements. 该用户重复参与了该实验。"},
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
                relationship = engagement.status

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
        description = request.data.get("description", "")
        person_wanted = request.data.get("person_wanted", 1)
        money_per_person = request.data.get("money_per_person", 1)
        activity_time = request.data.get("activity_time", "2024-01-01")
        activity_location = request.data.get("activity_location", "北京大学")
        image = request.data.get("image", "experiment/default.jpg")
        # TODO:类型检查

        tags = request.data.get("tags", 0)

        log_print(tags)
        tags = int(tags)

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
                tag = Tags.objects.get(id=tag_id)
                tagsexps = TagsExps(tags=tag, experiment=experiment)
                tagsexps.save()

            experiment.image = image
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

        final_set = Experiment.objects.filter(id__in=pre_set)

        experiments = final_set.filter(
            Q(title__contains=keyword) | Q(description__contains=keyword)
        ).order_by(orderby)

        # 分页处理
        paginator = ExperimentPagination()
        paginated_experiments = paginator.paginate_queryset(experiments, request)

        serializer = ExperimentDetailSerializer(paginated_experiments, many=True)
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

        serializer = ExperimentDetailSerializer(paginated_experiments, many=True)
        return paginator.get_paginated_response(serializer.data)


class ExperimentSearchInCreated(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            return Response(
                {"detail": "Authentication required. 该功能需要先登录。"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user = request.user
        tags = request.GET.get("tags", 0)
        keyword = request.GET.get("keyword", "")

        orderby = request.GET.get("orderby", "id")

        if hasattr(Experiment, orderby) == False:
            orderby = "id"

        sort = request.GET.get("sort", "asc")

        if sort == "desc":
            orderby = f"-{orderby}"  # 使用负号表示降序排序
        log_print("keyword:", keyword)
        # 先筛符合tag的

        pre_set = set(Experiment.objects.values_list("id", flat=True))

        pos = get_set_bits_positions(int(tags))

        for tag in pos:
            tagsexps = TagsExps.objects.filter(tags=tag).select_related("experiment")
            now_set = {instance.experiment.id for instance in tagsexps}
            log_print(type(pre_set), type(now_set))
            pre_set = pre_set.intersection(now_set)
        log_print(pre_set)

        final_set = Experiment.objects.filter(id__in=pre_set)

        experiments = final_set.filter(
            Q(creator=user)
            & (Q(title__contains=keyword) | Q(description__contains=keyword))
        ).order_by(orderby)

        # 分页处理
        paginator = ExperimentPagination()
        paginated_experiments = paginator.paginate_queryset(experiments, request)

        serializer = ExperimentDetailSerializer(paginated_experiments, many=True)
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

        serializer = ExperimentDetailSerializer(paginated_experiments, many=True)
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
        serializer = ExperimentDetailSerializer(experiment)
        response = Response(serializer.data)
        response.data["message"] = "Successfully close the experiment. 成功关闭实验。"
        return response


class ExperimentEdit(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        log_print(request.headers, request.data)
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
            Experiment.objects.filter(id=id).update(**attri)
            experiment = Experiment.objects.get(id=id)
            serializer = ExperimentDetailSerializer(experiment)
            response = Response(serializer.data)
            response.data["message"] = (
                "Experiment info edited successfully. 实验信息更新成功。"
            )
            return response

        except Exception:
            return Response(
                {"detail": "Format error. 有内容不符合格式。"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ExperimentImageUpload(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        log_print(request.headers, request.data)
        user = request.user
        if isinstance(request.user, AnonymousUser):
            return Response(
                {"detail": "Authentication required. 该功能需要先登录。"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        id = request.data.get("experiment")
        try:
            experiment = Experiment.objects.get(id=id)
        except Exception:
            return Response(
                {"detail": "The experiment doesn't exist. 该实验不存在。"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if experiment.creator != user:
            return Response(
                {
                    "detail": "Current user is not the experiment creator. 当前用户非实验创建者。"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        image = request.FILES.get("image")

        if not image:
            return Response(
                {"detail": "No file uploaded. 未上传文件。"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not image.content_type.startswith("image"):
            return Response(
                {"detail": "The file is not an image. 该文件不是图片。"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        fs = FileSystemStorage(location=settings.MEDIA_ROOT)  # 设置文件存储位置
        filename = GeneratePath.generate_path_experiment(experiment, image.name)
        filename = fs.save(filename, image)
        file_url = fs.url(filename).replace(settings.MEDIA_URL, "", 1)  # 保存文件

        experiment.image = file_url

        experiment.save()
        serializer = ExperimentDetailSerializer(experiment)
        return Response(serializer.data)

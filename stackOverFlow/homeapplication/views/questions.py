import logging

from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from stackOverFlow.homeapplication.error_codes import error_codes
from stackOverFlow.homeapplication.models import Question, TagsQuestion, User, QuestionUser
from stackOverFlow.homeapplication.serializers.questions import (
    QuestionSerializer, QuestionCreateSerializer, QuestionUpdateSerializer, TagsListSerializer,
    QuestionsByTagSerializer, TagsHotListSerializer, TagsSerializer, QuestionUserSerializer,
    QuestionUserStatusSerializer,
)

logger = logging.getLogger(__name__)


class QuestionViewSet(GenericViewSet):
    """问题贴视图"""
    queryset = Question.objects.filter()
    serializer_class = QuestionSerializer

    # id_parameter = openapi.Parameter('id', in_=openapi.IN_QUERY, description='question_id', type=openapi.TYPE_INTEGER)

    @atomic
    @swagger_auto_schema(
        request_body=QuestionCreateSerializer,
        tags=["问题 Question"],
        operation_summary="帖子创建"
    )
    def create(self, request):
        """
        帖子创建
        """
        try:
            question = Question.objects.create_question(request=request, validated_data=request.data)
        except Exception:
            logger.exception("问题贴创建失败")
            raise error_codes.QUESTION_CREATE_FAILED
        return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)

    @atomic
    @swagger_auto_schema(
        request_body=QuestionUpdateSerializer,
        tags=["问题 Question"],
        operation_summary="帖子更改"
    )
    def update(self, request, pk):
        """
        帖子更改
        """
        question = get_object_or_404(Question, pk=pk)
        try:
            Question.objects.update_question(request=request, validated_data=request.data, pk=pk)
        except Exception:
            logger.exception("问题贴修改失败")
            raise error_codes.QUESTION_UPDATE_FAILED
        return Response(QuestionSerializer(question).data, status=status.HTTP_200_OK)

    @atomic
    @swagger_auto_schema(
        tags=["问题 Question"],
        operation_summary="删帖"
    )
    def destroy(self, request, *arg, **kwargs):
        """删帖"""
        question = get_object_or_404(Question, pk=self.get_object().id)
        try:
            Question.objects.delete_question(request=request, question=question)
        except Exception:
            logger.exception("问题贴删除失败")
            raise error_codes.QUESTION_DELETE_FAILED
        return Response(QuestionSerializer(question).data, status=status.HTTP_204_NO_CONTENT)

    @atomic
    @swagger_auto_schema(
        tags=["问题 Question"],
        operation_summary="添加标签"
    )
    @action(detail=False, methods=["POST"])
    def add_tag(self, request, *args, **kwargs):
        try:
            tag = TagsQuestion.objects.update_or_create(tag=request.data["tag"])[0]
        except Exception:
            logger.exception("添加标签失败")
            raise error_codes.TAG_ADD_FAILED
        return Response(TagsSerializer(tag).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["问题 Question"],
        operation_summary="问题搜查"
    )
    def list(self, request, *args, **kwargs):
        try:
            questions = Question.objects.all_search(title=request.GET.get("title"))
        except Exception:
            logger.exception("问题搜查失败")
            raise error_codes.QUESTION_LIST_FAILED
        return Response(QuestionsByTagSerializer({"results": questions}).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["问题 Question"],
        operation_summary="根据问题ID获取问题"
    )
    @action(detail=False, methods=["GET"])
    def get_question(self, request, *args, **kwargs):
        try:
            question = get_object_or_404(Question, pk=request.GET.get("question_id"))
        except Exception:
            logger.exception("问题搜查失败")
            raise error_codes.QUESTION_LIST_FAILED
        return Response(QuestionSerializer(question).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["问题 Question"],
        operation_summary="获取相关问题列表"
    )
    @action(detail=True, methods=["POST"])
    def get_related_questions(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        try:
            related_questions = Question.objects.get_related_questions(question)
        except Exception:
            logger.exception("列出相关问题失败")
            raise error_codes.QUESTION_RELATED_LIST_FAILED
        return Response(QuestionsByTagSerializer({"results": related_questions}).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["问题 Question"],
        operation_summary="列出标签"
    )
    @action(detail=False, methods=["GET"])
    def list_tag(self, request, *args, **kwargs):
        try:
            tags_question = TagsQuestion.objects.find_all(data=request.GET.get("tag"))
        except Exception:
            logger.exception("列出标签失败")
            raise error_codes.TAG_LIST_FAILED
        return Response(TagsListSerializer({"results": tags_question}).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["问题 Question"],
        operation_summary="获取问题最多的五个标签"
    )
    @action(detail=False, methods=["GET"])
    def list_hot_tag(self, request, *args, **kwargs):
        try:
            tags_question = TagsQuestion.objects.list_hot_tag(request)
        except Exception:
            logger.exception("列出标签失败")
            raise error_codes.TAG_LIST_FAILED
        return Response(TagsHotListSerializer({"results": tags_question}).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["问题 Question"],
        operation_summary="标签获取问题"
    )
    @action(detail=True, methods=["POST"])
    def get_question_by_tag(self, request, pk):
        try:
            questions = Question.objects.filter(tag=self.get_object().tag)
        except Exception:
            logger.exception("标签获取问题失败")
            raise error_codes.TAG_QUESTION_LIST_FAILED
        return Response(QuestionsByTagSerializer({"results": questions}).data, status=status.HTTP_200_OK)

    @atomic
    @swagger_auto_schema(
        tags=["问题 Question"],
        operation_summary="赞问题贴"
    )
    @action(detail=True, methods=["POST"])
    def vote(self, request, pk):
        """
        赞问题贴
        """
        back_question = get_object_or_404(Question, pk=pk)
        try:
            question_user = Question.objects.vote_back(request=request, back_question=back_question)
        except Exception:
            logger.exception("赞问题贴更新失败")
            raise error_codes.QUESTION_USER_UPDATE_FAILED
        return Response(QuestionUserSerializer(question_user).data, status=status.HTTP_200_OK)

    @atomic
    @swagger_auto_schema(
        tags=["问题 Question"],
        operation_summary="否赞问题贴"
    )
    @action(detail=True, methods=["POST"])
    def down_vote(self, request, pk):
        """
        否赞问题贴
        """
        back_question = get_object_or_404(Question, pk=pk)
        try:
            question_user = Question.objects.down_vote_back(request=request, back_question=back_question)
        except Exception:
            logger.exception("否赞问题贴更新失败")
            raise error_codes.QUESTION_NO_USER_UPDATE_FAILED
        return Response(QuestionUserSerializer(question_user).data, status=status.HTTP_200_OK)

    @atomic
    @swagger_auto_schema(
        tags=["问题 Question"],
        operation_summary="获取问题用户赞同状态"
    )
    @action(detail=False, methods=["GET"])
    def get_vote_status(self, request, *args, **kwargs):
        try:
            question_user = QuestionUser.objects.filter(username=request.user.username, question_id=request.data["question_id"])
            if question_user.exists():
                status = question_user.status
            else:
                status = "zero"
        except Exception:
            logger.exception("状态获取失败")
            raise error_codes.QUESTION_USER_GET_STATUS_FAILED
        return Response(QuestionUserStatusSerializer(status).data, status=status.HTTP_200_OK)

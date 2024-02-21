import logging

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from homeapplication.error_codes import error_codes
from homeapplication.models import BackQuestion, BackUser
from homeapplication.serializers.back_question import (
    BackQuestionSerializer, BackQuestionCreateSerializer, BackQuestionUpdateSerializer, BackUserSerializer,
    BackListSerializer, BackUserStatusSerializer
)

logger = logging.getLogger(__name__)


class BackQuestionViewSet(ModelViewSet):
    """回帖视图"""
    queryset = BackQuestion.objects.filter()
    serializer_class = BackQuestionSerializer

    @swagger_auto_schema(operation_id=None)
    def not_implemented(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    update = retrieve = not_implemented

    def get_serializer_class(self):
        if self.action == "create":
            return BackQuestionCreateSerializer
        if self.action == 'update':
            return BackQuestionUpdateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        username = self.request.user.username
        serializer.save(username=username)

    @atomic
    @swagger_auto_schema(
        tags=["回帖 BackQuestion"],
        operation_summary="回帖创建"
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    # @atomic
    # @swagger_auto_schema(
    #     tags=["回帖 BackQuestion"],
    #     operation_summary="回帖创建"
    # )
    # def create(self, request, *args, **kwargs):
    #     """
    #     回帖创建
    #     """
    #     return super().create(request, *args, **kwargs)
        # try:
        #     question = BackQuestion.objects.create_back_question(request=request, validated_data=request.data)
        # except Exception:
        #     logger.exception("回帖创建失败")
        #     raise error_codes.BACK_QUESTION_CREATE_FAILED
        # return Response(self.get_serializer(question).data, status=status.HTTP_201_CREATED)

    @atomic
    @swagger_auto_schema(
        tags=["回帖 BackQuestion"],
        operation_summary="跟帖更改"
    )
    def update(self, request, *args, **kwargs):
        """
        跟帖更改
        """
        # print(kwargs.get('pk')) 获取URL中传入的ID，request.data["pk"]并不行
        back_question = get_object_or_404(BackQuestion, pk=kwargs.get('pk'))
        try:
            BackQuestion.objects.update_back_question(request=request, validated_data=request.data)
        except Exception:
            logger.exception("回帖更改失败")
            raise error_codes.BACK_QUESTION_UPDATE_FAILED
        return Response(self.get_serializer(back_question).data, status=status.HTTP_200_OK)

    @atomic
    @swagger_auto_schema(
        tags=["回帖 BackQuestion"],
        operation_summary="删回帖"
    )
    def destroy(self, request, *arg, **kwargs):
        """删回帖"""
        back_question = get_object_or_404(BackQuestion, pk=self.get_object().id)
        try:
            BackQuestion.objects.delete_back_question(request=request, back_question=back_question)
        except Exception:
            logger.exception("回帖删除失败")
            raise error_codes.BACK_QUESTION_DELETE_FAILED
        return Response(self.get_serializer(back_question).data, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        tags=["回帖 BackQuestion"],
        operation_summary="回帖列表"
    )
    def list(self, request, *args, **kwargs):
        pk = request.query_params.get('question_id', None)
        if not pk:
            raise error_codes.BACK_QUESTION_LIST_NEED_QUESTION_ID
        try:
            back_questions = BackQuestion.objects.back_list(pk=pk)
        except Exception:
            logger.exception("列出回帖失败")
            raise error_codes.BACK_QUESTION_LIST_FAILED
        return Response(BackListSerializer(back_questions).data, status=status.HTTP_200_OK)

    @atomic
    @swagger_auto_schema(
        tags=["回帖 BackQuestion"],
        operation_summary="回帖"
    )
    @action(detail=True, methods=["POST"])
    def vote_back(self, request, pk):
        """
        回帖赞同否
        """
        back_question = get_object_or_404(BackQuestion, pk=pk)
        try:
            back_user = BackQuestion.objects.vote_back(request=request, back_question=back_question)
        except Exception:
            logger.exception("回帖状态赞同更新失败")
            raise error_codes.BACK_QUESTION_USER_UPDATE_FAILED
        return Response(BackUserSerializer(back_user).data, status=status.HTTP_200_OK)

    @atomic
    @swagger_auto_schema(
        tags=["回帖 BackQuestion"],
        operation_summary="回帖"
    )
    @action(detail=True, methods=["POST"])
    def down_vote_back(self, request, pk):
        """
        回帖不赞同否
        """
        back_question = get_object_or_404(BackQuestion, pk=pk)
        try:
            back_user = BackQuestion.objects.down_vote_back(request=request, back_question=back_question)
        except Exception:
            logger.exception("回帖状态不赞同更新失败")
            raise error_codes.BACK_QUESTION_NO_USER_UPDATE_FAILED
        return Response(BackUserSerializer(back_user).data, status=status.HTTP_200_OK)

    @atomic
    @swagger_auto_schema(
        tags=["回帖 BackQuestion"],
        operation_summary="获取回帖用户赞同状态"
    )
    @action(detail=False, methods=["GET"])
    def get_vote_back_status(self, request, *args, **kwargs):
        try:
            question_user = BackUser.objects.filter(username=request.user.username, question_id=request.data["back_question_id"])
            if question_user.exists():
                status = question_user.status
            else:
                status = "zero"
        except Exception:
            logger.exception("回帖状态获取失败")
            raise error_codes.BACK_QUESTION_USER_GET_STATUS_FAILED
        return Response(BackUserStatusSerializer(status).data, status=status.HTTP_200_OK)

    @atomic
    @swagger_auto_schema(
        tags=["回帖 BackQuestion"],
        operation_summary="根据问题ID获取回帖"
    )
    @action(detail=True, methods=["GET"])
    def get_back_by_question(self, request, pk):
        try:
            back_questions = BackQuestion.objects.filter(question_id=pk)
        except Exception:
            logger.exception("列出回帖失败")
            raise error_codes.BACK_QUESTION_LIST_FAILED
        return Response(BackListSerializer({"results": back_questions}).data, status=status.HTTP_200_OK)

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
from stackOverFlow.homeapplication.models import BackQuestion, Question
from stackOverFlow.homeapplication.serializers.back_question import (
    BackQuestionSerializer, BackQuestionCreateSerializer, BackQuestionUpdateSerializer, BackUserSerializer
)

logger = logging.getLogger(__name__)


class BackQuestionViewSet(GenericViewSet):
    """回帖视图"""
    queryset = BackQuestion.objects.filter()
    serializer_class = BackQuestionSerializer

    @atomic
    @swagger_auto_schema(
        request_body=BackQuestionCreateSerializer,
        tags=["回帖 BackQuestion"],
        operation_summary="回帖"
    )
    def create(self, request):
        """
        回帖创建
        """
        get_object_or_404(Question, pk=request.data["question_id"])
        try:
            question = BackQuestion.objects.create_back_question(request=request, validated_data=request.data)
        except Exception:
            logger.exception("回帖创建失败")
            raise error_codes.BACK_QUESTION_CREATE_FAILED
        return Response(self.get_serializer(question).data, status=status.HTTP_201_CREATED)

    @atomic
    @swagger_auto_schema(
        request_body=BackQuestionUpdateSerializer,
        tags=["回帖 BackQuestion"],
        operation_summary="回帖"
    )
    def update(self, request, pk):
        """
        跟帖更改
        """
        back_question = get_object_or_404(BackQuestion, pk=pk)
        try:
            BackQuestion.objects.update_back_question(request=request, validated_data=request.data)
        except Exception:
            logger.exception("回帖更改失败")
            raise error_codes.BACK_QUESTION_UPDATE_FAILED
        return Response(self.get_serializer(back_question).data, status=status.HTTP_200_OK)

    @atomic
    @swagger_auto_schema(
        tags=["回帖 BackQuestion"],
        operation_summary="回帖"
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

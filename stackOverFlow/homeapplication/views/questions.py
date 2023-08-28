import logging

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from stackOverFlow.homeapplication.error_codes import error_codes
from stackOverFlow.homeapplication.models import Question
from stackOverFlow.homeapplication.serializers.questions import (
    QuestionSerializer,
    QuestionCreateSerializer,
    QuestionUpdateSerializer
)

logger = logging.getLogger(__name__)


class QuestionViewSet(GenericViewSet):
    """用户注册视图"""
    queryset = Question.objects.filter()
    serializer_class = QuestionSerializer

    @atomic
    @swagger_auto_schema(
        request_body=QuestionCreateSerializer,
        tags=["问题 Question"],
        operation_summary="问题"
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
        operation_summary="问题"
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

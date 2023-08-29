import logging

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from stackOverFlow.homeapplication.error_codes import error_codes
from stackOverFlow.homeapplication.models import FollowQuestion, Question, BackQuestion
from stackOverFlow.homeapplication.serializers.follow_question import (
    FollowQuestionSerializer,
    FollowQuestionCreateSerializer
)

logger = logging.getLogger(__name__)


class FollowQuestionViewSet(GenericViewSet):
    """跟帖视图"""
    queryset = FollowQuestion.objects.filter()
    serializer_class = FollowQuestionSerializer

    @atomic
    @swagger_auto_schema(
        request_body=FollowQuestionCreateSerializer,
        tags=["跟帖 FollowQuestion"],
        operation_summary="跟帖"
    )
    def create(self, request):
        """
        跟帖创建
        """
        get_object_or_404(BackQuestion, pk=request.data["back_question_id"])
        try:
            question = FollowQuestion.objects.create_follow_question(request=request, validated_data=request.data)
        except Exception:
            logger.exception("跟帖创建失败")
            raise error_codes.QUESTION_CREATE_FAILED
        return Response(self.get_serializer(question).data, status=status.HTTP_201_CREATED)

    @atomic
    @swagger_auto_schema(
        tags=["跟帖 FollowQuestion"],
        operation_summary="跟帖"
    )
    def destroy(self, request, *arg, **kwargs):
        """删跟帖"""
        back_question = get_object_or_404(BackQuestion, pk=self.get_object().id)
        try:
            FollowQuestion.objects.delete_follow_question(request=request, back_question=back_question)
        except Exception:
            logger.exception("问题贴删除失败")
            raise error_codes.QUESTION_DELETE_FAILED
        return Response(self.get_serializer(back_question).data, status=status.HTTP_204_NO_CONTENT)

from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers

from stackOverFlow.homeapplication.models import BackQuestion, Question


class BackQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackQuestion
        fields = "__all__"


class BackQuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackQuestion
        exclude = ["user_id"]


class BackQuestionUpdateSerializer(serializers.Serializer):
    content = serializers.CharField(help_text="内容")

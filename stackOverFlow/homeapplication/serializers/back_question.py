from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers

from stackOverFlow.homeapplication.models import BackQuestion, Question, BackUser


class BackQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackQuestion
        fields = "__all__"


class BackQuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackQuestion
        exclude = ["user_id", "upvotes", "downvotes"]


class BackQuestionUpdateSerializer(serializers.Serializer):
    content = serializers.CharField(help_text="内容")


class BackListSerializer(serializers.Serializer):
    results = BackQuestionSerializer(many=True, help_text="回帖列表")


class BackUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackUser
        fields = "__all__"

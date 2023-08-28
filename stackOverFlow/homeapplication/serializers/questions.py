from rest_framework import serializers

from stackOverFlow.homeapplication.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class QuestionCreateSerializer(serializers.Serializer):
    title = serializers.CharField(help_text="标题", max_length=100)
    content = serializers.CharField(help_text="内容")
    tag = serializers.CharField(help_text="标签名称", default="默认")


class QuestionUpdateSerializer(serializers.Serializer):
    question_id = serializers.IntegerField(help_text="问题ID")
    title = serializers.CharField(help_text="标题", max_length=100, required=False)
    content = serializers.CharField(help_text="内容", required=False)
    tag = serializers.CharField(help_text="标签名称", required=False)

from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers

from stackOverFlow.homeapplication.models import BackQuestion, Question, BackUser, User


class BackQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackQuestion
        fields = "__all__"


class BackQuestionCreateSerializer(BackQuestionSerializer):
    class Meta(BackQuestionSerializer.Meta):
        read_only_fields = ["username", "upvotes", "downvotes"]

    def validate_question_id(self, value):
        if not Question.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid question_id.")
        return value

    def save(self, **kwargs):
        # Your custom logic here
        user = User.objects.get(username=kwargs["username"])
        user.back_question += 1
        user.save()
        # Call the superclass's save method
        return super().save(**kwargs)


class BackQuestionUpdateSerializer(BackQuestionSerializer):
    class Meta(BackQuestionSerializer.Meta):
        read_only_fields = [f.name for f in BackQuestion._meta.fields if f.name not in ["content"]]


class BackListSerializer(serializers.Serializer):
    results = BackQuestionSerializer(many=True, help_text="回帖列表")


class BackUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackUser
        fields = "__all__"


class BackUserStatusSerializer(serializers.Serializer):
    status = serializers.CharField(help_text="赞同状态")

from rest_framework import serializers

from stackOverFlow.homeapplication.models import FollowQuestion


class FollowQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowQuestion
        fields = "__all__"


class FollowQuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowQuestion
        exclude = ["username"]

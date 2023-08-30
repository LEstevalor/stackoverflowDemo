import logging

from django.db import models

logger = logging.getLogger(__name__)


class FollowQuestionManager(models.Manager):
    """跟帖管理"""
    def create_follow_question(self, request, validated_data):
        """创建跟帖"""
        from stackOverFlow.homeapplication.models import User
        user = User.objects.get(username=request.user.username)
        user.follow_question += 1
        user.save()
        validated_data["username"] = user.username
        return super().create(**validated_data)

    def delete_follow_question(self, request, back_question):
        """删除跟帖"""
        from stackOverFlow.homeapplication.models import User
        user = User.objects.get(username=request.user.username)
        user.follow_question -= 1
        user.save()
        return back_question.delete()

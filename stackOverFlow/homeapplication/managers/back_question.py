import logging

from django.db import models

logger = logging.getLogger(__name__)


class BackQuestionManager(models.Manager):
    """回贴管理"""
    def create_back_question(self, request, validated_data):
        """创建回帖"""
        from stackOverFlow.homeapplication.models import User
        user = User.objects.get(username=request.user.username)
        user.back_question += 1
        user.save()
        validated_data["user_id"] = user.id
        return super().create(**validated_data)

    def update_back_question(self, request, validated_data):
        """更新回帖"""
        return super().update(**validated_data)

    def delete_back_question(self, request, back_question):
        """删除回帖"""
        from stackOverFlow.homeapplication.models import User, FollowQuestion
        user = User.objects.get(username=request.user.username)
        user.back_question -= 1
        user.save()

        FollowQuestion.objects.filter(back_question_id=back_question.id).delete()
        return back_question.delete()

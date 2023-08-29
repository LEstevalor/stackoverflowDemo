import logging

from django.db import models

logger = logging.getLogger(__name__)


class QuestionManager(models.Manager):
    """问题贴管理"""
    def create_question(self, request, validated_data):
        """创建问题"""
        from stackOverFlow.homeapplication.models import User, TagsQuestion
        user = User.objects.get(username=request.user.username)
        user.question_count += 1
        user.save()

        if validated_data.get("tag"):
            tags_question = TagsQuestion.objects.filter(tag=validated_data["tag"])
            if not tags_question.exists():
                TagsQuestion.objects.create(tag=validated_data["tag"])

        validated_data["user_id"] = user.id
        return super().create(**validated_data)

    def update_question(self, request, validated_data, pk):
        """更新问题"""
        from stackOverFlow.homeapplication.models import TagsQuestion
        if validated_data.get("tag"):
            tags_question = TagsQuestion.objects.filter(tag=validated_data["tag"])
            if not tags_question.exists():
                TagsQuestion.objects.create(tag=validated_data["tag"])
        return super().update(**validated_data)

    def delete_question(self, request, question):
        """删除帖"""
        from stackOverFlow.homeapplication.models import User, BackQuestion, FollowQuestion
        user = User.objects.get(username=request.user.username)
        user.question_count -= 1
        user.save()

        back_question = BackQuestion.objects.filter(question_id=question.id)
        FollowQuestion.objects.filter(back_question__in=back_question.values_list("id", flat=True))
        back_question.delete()
        return question.delete()

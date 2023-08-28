from django.db import models

from stackOverFlow.base import BaseModel


class FollowQuestion(BaseModel):
    """跟帖模型"""
    content = models.TextField(verbose_name="内容")
    user_id = models.IntegerField(verbose_name="用户ID")
    upvotes = models.IntegerField(verbose_name="赞成数", default=0)
    downvotes = models.IntegerField(verbose_name="反对数", default=0)
    question_id = models.IntegerField(verbose_name="问题ID")

    class Meta:
        db_table = 'sof_follow_question'
        verbose_name = "跟帖表"
        verbose_name_plural = verbose_name

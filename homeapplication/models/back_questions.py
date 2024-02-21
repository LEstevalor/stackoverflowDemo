from django.db import models

from stackOverFlow.base import BaseModel
from homeapplication.constants.model_constants import BackUserStatus
from homeapplication.managers.back_question import BackQuestionManager


class BackQuestion(BaseModel):
    """回帖模型"""
    content = models.TextField(verbose_name="内容")
    username = models.CharField(verbose_name="作者", max_length=20)
    question_id = models.IntegerField(verbose_name="问题ID", null=True)
    upvotes = models.IntegerField(verbose_name="赞成数", default=0)
    downvotes = models.IntegerField(verbose_name="反对数", default=0)

    objects = BackQuestionManager()

    class Meta:
        db_table = 'sof_back_question'
        verbose_name = "回帖表"
        verbose_name_plural = verbose_name


class BackUser(models.Model):
    """回帖中用户赞同或不赞同"""
    username = models.CharField(verbose_name="作者", max_length=20)
    back_question_id = models.IntegerField(verbose_name="回帖ID")
    status = models.CharField(
        "赞同状态", max_length=10, choices=BackUserStatus.get_choices(), default=BackUserStatus.ZERO.value
    )

    class Meta:
        db_table = 'sof_back_user'
        verbose_name = "回帖用户状态表"
        verbose_name_plural = verbose_name

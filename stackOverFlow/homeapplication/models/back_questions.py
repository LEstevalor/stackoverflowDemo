from django.db import models

from stackOverFlow.base import BaseModel
from stackOverFlow.homeapplication.managers.back_question import BackQuestionManager


class BackQuestion(BaseModel):
    """回帖模型"""
    content = models.TextField(verbose_name="内容")
    user_id = models.IntegerField(verbose_name="用户ID")
    question_id = models.IntegerField(verbose_name="问题ID", null=True)

    objects = BackQuestionManager()

    class Meta:
        db_table = 'sof_back_question'
        verbose_name = "回帖表"
        verbose_name_plural = verbose_name

from django.db import models

from stackOverFlow.base import BaseModel


class BackQuestion(BaseModel):
    """回帖模型"""
    content = models.TextField(verbose_name="内容")
    user_id = models.IntegerField(verbose_name="用户ID")

    class Meta:
        db_table = 'sof_back_question'
        verbose_name = "回帖表"
        verbose_name_plural = verbose_name

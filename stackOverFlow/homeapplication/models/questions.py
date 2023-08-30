from django.db import models

from stackOverFlow.base import BaseModel
from stackOverFlow.homeapplication.managers.questions import QuestionManager, TagsQuestionManager


class TagsQuestion(BaseModel):
    """标签类"""
    tag = models.CharField(verbose_name="标签名称", max_length=25, db_index=True)

    objects = TagsQuestionManager()

    class Meta:
        db_table = 'sof_tags_question'
        verbose_name = "问题标签表"
        verbose_name_plural = verbose_name


class Question(BaseModel):
    """问题模型"""
    title = models.CharField(verbose_name="标题", max_length=100, unique=True)
    content = models.TextField(verbose_name="内容")
    user_id = models.IntegerField(verbose_name="作者ID")
    tag = models.CharField(verbose_name="标签名称", max_length=25, null=True)

    objects = QuestionManager()

    class Meta:
        db_table = 'sof_question'
        verbose_name = "问题表"
        verbose_name_plural = verbose_name


class UserViewQuestion(BaseModel):
    """用户问题浏览"""
    user_id = models.IntegerField(verbose_name="用户ID")
    question_id = models.IntegerField(verbose_name="帖子ID")

    class Meta:
        db_table = 'sof_user_question'
        verbose_name = "用户问题表"
        verbose_name_plural = verbose_name

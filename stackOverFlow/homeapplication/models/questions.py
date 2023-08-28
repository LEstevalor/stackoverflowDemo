from django.db import models

from stackOverFlow.base import BaseModel


class TagsQuestion(BaseModel):
    """标签类"""
    tag = models.CharField(verbose_name="标签名称", max_length=25)

    class Meta:
        db_table = 'sof_tags_question'
        verbose_name = "问题标签表"
        verbose_name_plural = verbose_name


class Question(BaseModel):
    """问题模型"""
    title = models.CharField(verbose_name="标题", max_length=100)
    content = models.TextField(verbose_name="内容")
    user_id = models.IntegerField(verbose_name="作者ID")
    tag_id = models.IntegerField(verbose_name="标签ID")

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

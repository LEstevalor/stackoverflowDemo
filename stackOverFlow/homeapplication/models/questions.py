from django.db import models

from stackOverFlow.base import BaseModel
from stackOverFlow.homeapplication.constants.model_constants import BackUserStatus
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
    username = models.CharField(verbose_name="作者", max_length=20)
    tag = models.CharField(verbose_name="标签名称", max_length=25, null=True)
    upvotes = models.IntegerField(verbose_name="赞成数", default=0)
    downvotes = models.IntegerField(verbose_name="反对数", default=0)

    objects = QuestionManager()

    class Meta:
        db_table = 'sof_question'
        verbose_name = "问题表"
        verbose_name_plural = verbose_name


class QuestionUser(models.Model):
    """问题帖中用户赞同或不赞同"""
    username = models.CharField(verbose_name="作者", max_length=20)
    question_id = models.IntegerField(verbose_name="问题贴ID")
    status = models.CharField(
        "赞同状态", max_length=10, choices=BackUserStatus.get_choices(), default=BackUserStatus.ZERO.value
    )

    class Meta:
        db_table = 'sof_question_user'
        verbose_name = "问题贴用户状态表"
        verbose_name_plural = verbose_name


class UserViewQuestion(BaseModel):
    """用户问题浏览"""
    username = models.CharField(verbose_name="作者", max_length=20)
    question_id = models.IntegerField(verbose_name="帖子ID")

    class Meta:
        db_table = 'sof_user_question'
        verbose_name = "用户问题表"
        verbose_name_plural = verbose_name

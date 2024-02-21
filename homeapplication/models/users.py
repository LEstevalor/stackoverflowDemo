from django.contrib.auth.models import AbstractUser
from django.db import models

from homeapplication.managers.users import UserManager


class User(AbstractUser):
    """自定义用户模型类"""
    # 账号（唯一） 密码 电话 邮箱（唯一） 用户级别
    # username = models.CharField(max_length=100)
    # password = models.CharField(max_length=100)
    # email = models.EmailField()
    username = models.CharField(verbose_name="作者", max_length=20, db_index=True, unique=True)
    question_count = models.IntegerField(default=0, verbose_name="发帖数")
    follow_question = models.IntegerField(default=0, verbose_name="跟帖数")
    back_question = models.IntegerField(default=0, verbose_name="回帖数")

    objects = UserManager()

    class Meta:
        db_table = 'sof_user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
        # 元数据主要用在管理后台的展示上，verbose_name_plural 是模型类的复数名 。
        # 如果不设置的话，Django 会使用小写的模型名作为默认值，并且在结尾加上 s。通过此项元数据设置名字可以去掉 s。


class UserImage(models.Model):
    username = models.CharField(verbose_name="作者", max_length=20, db_index=True, unique=True)
    image = models.BinaryField(verbose_name="用户头像")

    class Meta:
        db_table = 'sof_user_images'
        verbose_name = "用户头像表"
        verbose_name_plural = verbose_name

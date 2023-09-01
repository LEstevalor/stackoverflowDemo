import logging

from django.db import models
from django.db.models import ExpressionWrapper, F, IntegerField

from stackOverFlow.homeapplication.constants.model_constants import BackUserStatus

logger = logging.getLogger(__name__)


class BackQuestionManager(models.Manager):
    """回贴管理"""
    def create_back_question(self, request, validated_data):
        """创建回帖"""
        from stackOverFlow.homeapplication.models import User
        user = User.objects.get(username=request.user.username)
        user.back_question += 1
        user.save()
        validated_data["username"] = user.username
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

    def back_list(self, request, pk):
        """搜寻回帖"""
        # F 表达式计算同表中 upvotes 和 downvotes 之间的差值
        diff = ExpressionWrapper(F('upvotes') - F('downvotes'), output_field=IntegerField())
        # 根据差值对查询结果进行排序
        lists = self.filter(question_id=pk).annotate(difference=diff).order_by('-difference')
        return lists

    def vote_back(self, request, back_question):
        """赞贴"""
        from stackOverFlow.homeapplication.models import User, BackUser
        back_user = BackUser.objects.filter(username=request.user.username, back_question_id=back_question.id).first()
        # 已经是点赞状态则返回ZERO状态
        if back_user.status == BackUserStatus.UPVOTE.value:
            back_user.status = BackUserStatus.ZERO.value
            back_user.save()
            back_question.upvotes -= 1
        else:
            back_user = BackUser.objects.update_or_create(username=request.user.username, back_question_id=back_question.id,
                                                          status=BackUserStatus.UPVOTE.value)
            back_question.upvotes += 1
        back_question.save()
        return back_user

    def down_vote_back(self, request, back_question):
        """否贴"""
        from stackOverFlow.homeapplication.models import BackUser
        back_user = BackUser.objects.filter(username=request.user.username, back_question_id=back_question.id).first()
        # 已经是点赞状态则返回ZERO状态
        if back_user.status == BackUserStatus.DOWNVOTE.value:
            back_user.status = BackUserStatus.ZERO.value
            back_user.save()
            back_question.downvotes -= 1
        else:
            back_user = BackUser.objects.update_or_create(username=request.user.username, back_question_id=back_question.id,
                                                          status=BackUserStatus.DOWNVOTE.value)
            back_question.downvotes += 1
        back_question.save()
        return back_user

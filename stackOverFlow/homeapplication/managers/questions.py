import logging

from django.db import models
from django.db.models import Q, ExpressionWrapper, F, IntegerField
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from stackOverFlow.homeapplication.constants.model_constants import BackUserStatus

logger = logging.getLogger(__name__)


class QuestionManager(models.Manager):
    """问题贴管理"""
    def create_question(self, validated_data):
        """创建问题"""
        from stackOverFlow.homeapplication.models import User, TagsQuestion
        user = User.objects.get(username=validated_data["username"])
        user.question_count += 1
        user.save()

        if validated_data.get("tag"):
            tags_question = TagsQuestion.objects.filter(tag=validated_data["tag"])
            if not tags_question.exists():
                TagsQuestion.objects.create(tag=validated_data["tag"])

        validated_data["username"] = user.username
        return super().create(**validated_data)

    def update_question(self, validated_data, pk):
        """更新问题"""
        from stackOverFlow.homeapplication.models import TagsQuestion
        if validated_data.get("tag"):
            tags_question = TagsQuestion.objects.filter(tag=validated_data["tag"])
            if not tags_question.exists():
                TagsQuestion.objects.create(tag=validated_data["tag"])
        question = self.filter(id=pk)
        question.update(**validated_data)

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

    def all_search(self, request):
        """查询贴（包含题目的模糊查询）"""
        title = request.GET.get("title")
        time_sort = request.GET.get("time_sort")
        hot_sort = request.GET.get("hot_sort")
        if title:
            return self.filter(Q(title__icontains=title))
        elif time_sort:
            return self.all().order_by('-update_time')[:5]
        elif hot_sort:
            # 赞成-反对数做前五排序
            diff = ExpressionWrapper(F('upvotes') - F('downvotes'), output_field=IntegerField())
            return self.all().annotate(difference=diff).order_by('-difference')[:5]
        return self.all()

    def get_related_questions(self, question, limit=5):
        """相关性分析获取问题列表"""
        from stackOverFlow.homeapplication.models import Question
        all_questions = Question.objects.exclude(id=question.id)
        titles = [question.title] + [q.title for q in all_questions]
        # 标题转换为向量
        vectorizer = TfidfVectorizer()
        # 计算给定问题标题与所有其他问题标题之间的相似性
        title_vectors = vectorizer.fit_transform(titles)
        similarities = cosine_similarity(title_vectors[0:1], title_vectors[1:])
        # 进行排序并限制结果数量
        sorted_indices = similarities.argsort().flatten()
        top_indices = sorted_indices[-limit:]
        related_questions = [all_questions[int(i)] for i in top_indices]
        return related_questions

    def vote_back(self, request, question):
        """赞问题贴"""
        from stackOverFlow.homeapplication.models import QuestionUser
        back_user = QuestionUser.objects.filter(username=request.user.username, back_question_id=question.id).first()
        # 已经是点赞状态则返回ZERO状态
        if back_user.status == BackUserStatus.UPVOTE.value:
            back_user.status = BackUserStatus.ZERO.value
            back_user.save()
            question.upvotes -= 1
        else:
            back_user = QuestionUser.objects.update_or_create(username=request.user.username, back_question_id=question.id,
                                                              status=BackUserStatus.UPVOTE.value)
            question.upvotes += 1
        question.save()
        return back_user

    def down_vote_back(self, request, question):
        """否赞问题贴"""
        from stackOverFlow.homeapplication.models import QuestionUser
        back_user = QuestionUser.objects.filter(username=request.user.username, back_question_id=question.id).first()
        # 已经是点赞状态则返回ZERO状态
        if back_user.status == BackUserStatus.DOWNVOTE.value:
            back_user.status = BackUserStatus.ZERO.value
            back_user.save()
            question.downvotes -= 1
        else:
            back_user = QuestionUser.objects.update_or_create(username=request.user.username, back_question_id=question.id,
                                                              status=BackUserStatus.DOWNVOTE.value)
            question.downvotes += 1
        question.save()
        return back_user


class TagsQuestionManager(models.Manager):
    def list_hot_tag(self, request):
        """获取问题最多的五个标签"""
        from stackOverFlow.homeapplication.models import Question
        tag_list = self.all()

        tag_counts = []
        for tag in tag_list:
            tag.count = Question.objects.filter(tag=tag.tag).count()
            tag_counts.append(tag)

        num = request.GET.get("num")
        if not num:
            num = 5
        num = int(num)
        if num <= 100:
            # 按问题数量降序排序，并获取前五个标签
            top_five_tags = sorted(tag_counts, key=lambda x: x.count, reverse=True)[:num]
        else:
            top_five_tags = tag_counts
        return top_five_tags

    def list_tag_and_count(self, tag):
        """列出标签加贴数"""
        from stackOverFlow.homeapplication.models import Question
        if tag:
            tag_list = self.filter(Q(tag__icontains=tag))
        else:
            tag_list = self.all()
        for tag in tag_list:
            tag.count = Question.objects.filter(tag=tag.tag).count()
        return tag_list

    def find_all(self, data):
        """全局搜索tag或模糊搜索tag"""
        if not data:
            return self.all()
        return self.filter(tag__icontains=data)

    def find_single(self, tag):
        """搜索单tag"""
        from stackOverFlow.homeapplication.models import Question
        tag.count = Question.objects.filter(tag=tag.tag).count()
        return tag

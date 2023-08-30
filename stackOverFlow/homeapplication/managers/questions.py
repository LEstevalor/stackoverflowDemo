import logging

from django.db import models
from django.db.models import Count
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


class QuestionManager(models.Manager):
    """问题贴管理"""
    def create_question(self, request, validated_data):
        """创建问题"""
        from stackOverFlow.homeapplication.models import User, TagsQuestion
        user = User.objects.get(username=request.user.username)
        user.question_count += 1
        user.save()

        if validated_data.get("tag"):
            tags_question = TagsQuestion.objects.filter(tag=validated_data["tag"])
            if not tags_question.exists():
                TagsQuestion.objects.create(tag=validated_data["tag"])

        validated_data["user_id"] = user.id
        return super().create(**validated_data)

    def update_question(self, request, validated_data, pk):
        """更新问题"""
        from stackOverFlow.homeapplication.models import TagsQuestion
        if validated_data.get("tag"):
            tags_question = TagsQuestion.objects.filter(tag=validated_data["tag"])
            if not tags_question.exists():
                TagsQuestion.objects.create(tag=validated_data["tag"])
        return super().update(**validated_data)

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

    def get_related_questions(self, question, limit=10):
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
        related_questions = [all_questions[i] for i in top_indices]
        return related_questions


class TagsQuestionManager(models.Manager):
    def list_hot_tag(self, request):
        """获取问题最多的五个标签"""
        from stackOverFlow.homeapplication.models import Question
        tag_list = self.all()

        tag_counts = []
        for tag in tag_list:
            tag.count = Question.objects.filter(tag__icontains=tag.tag).count()
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

    def find_all(self, data):
        """全局搜索tag或模糊搜索tag"""
        if not data:
            return self.all()
        return self.filter(tag__icontains=data)

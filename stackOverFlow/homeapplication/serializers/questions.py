from rest_framework import serializers

from stackOverFlow.homeapplication.models import Question, TagsQuestion, QuestionUser


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class QuestionCreateSerializer(serializers.Serializer):
    title = serializers.CharField(help_text="标题", max_length=100)
    content = serializers.CharField(help_text="内容")
    tag = serializers.CharField(help_text="标签名称", default="默认")


class QuestionUpdateSerializer(serializers.Serializer):
    question_id = serializers.IntegerField(help_text="问题ID")
    title = serializers.CharField(help_text="标题", max_length=100, required=False)
    content = serializers.CharField(help_text="内容", required=False)
    tag = serializers.CharField(help_text="标签名称", required=False)


class QuestionDestroySerializer(serializers.Serializer):
    question_id = serializers.IntegerField(help_text="问题ID")


class QuestionsByTagSerializer(serializers.Serializer):
    results = QuestionSerializer(many=True, help_text="问题列表")


class QuestionUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionUser
        fields = "__all__"


class QuestionUserStatusSerializer(serializers.Serializer):
    status = serializers.CharField(help_text="赞同状态")


# 标签型序列化器
class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagsQuestion
        fields = "__all__"


class TagsListSerializer(serializers.Serializer):
    results = TagsSerializer(many=True, help_text="标签列表")


class TagsHotSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(help_text="标签下问题数", default=0)

    class Meta:
        model = TagsQuestion
        fields = "__all__"


class TagsHotListSerializer(serializers.Serializer):
    results = TagsHotSerializer(many=True, help_text="热门标签列表")

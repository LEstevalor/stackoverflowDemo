from blue_krill.data_types.enum import EnumField, StructuredEnum


class BackUserStatus(StructuredEnum):
    """回帖用户赞同状态"""
    UPVOTE = EnumField("upvote", label="赞同")
    ZERO = EnumField("zero", label="未赞同不赞同")
    DOWNVOTE = EnumField("downvote", label="不赞同")

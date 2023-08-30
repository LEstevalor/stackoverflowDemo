from blue_krill.web.std_error import ErrorCode


class ErrorCodes:
    # 用户
    USER_CREATE_FAILED = ErrorCode("用户注册失败")
    SENR_EMAIL_FAILED = ErrorCode("邮箱发送失败")
    EMAIL_VERIFY_FAILED = ErrorCode("邮箱验证有误")
    # 问题贴
    QUESTION_CREATE_FAILED = ErrorCode("问题贴创建失败")
    QUESTION_UPDATE_FAILED = ErrorCode("问题贴修改失败")
    QUESTION_DELETE_FAILED = ErrorCode("问题贴删除失败")
    TAG_QUESTION_LIST_FAILED = ErrorCode("标签获取问题失败")
    QUESTION_LIST_FAILED = ErrorCode("问题搜查失败")
    QUESTION_RELATED_LIST_FAILED = ErrorCode("列出相关问题失败")
    TAG_LIST_FAILED = ErrorCode("列出标签失败")
    TAG_ADD_FAILED = ErrorCode("添加标签失败")
    # 回帖
    BACK_QUESTION_CREATE_FAILED = ErrorCode("回帖创建失败")
    BACK_QUESTION_UPDATE_FAILED = ErrorCode("回帖更改失败")
    BACK_QUESTION_DELETE_FAILED = ErrorCode("回帖删除失败")
    BACK_QUESTION_USER_UPDATE_FAILED = ErrorCode("回帖状态赞同更新失败")
    BACK_QUESTION_NO_USER_UPDATE_FAILED = ErrorCode("回帖状态不赞同更新失败")
    BACK_QUESTION_LIST_FAILED = ErrorCode("列出回帖失败")
    BACK_QUESTION_LIST_NEED_QUESTION_ID = ErrorCode("列出回帖需要问题信息")


    def dump(self, fh=None):
        """A function to dump ErrorCodes as markdown table."""
        attrs = [attr for attr in dir(self) if attr.isupper()]
        table = {}
        for attr in attrs:
            code = getattr(self, attr)
            if code.code_num == -1:
                continue
            table[code.code_num] = code.message

        print("| 错误码 | 描述 |", file=fh)
        print("| - | - |", file=fh)
        for code_num, message in sorted(table.items()):
            print(f"| {code_num} | {message} |", file=fh)


error_codes = ErrorCodes()

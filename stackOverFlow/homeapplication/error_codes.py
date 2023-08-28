from blue_krill.web.std_error import ErrorCode


class ErrorCodes:
    # 用户
    USER_CREATE_FAILED = ErrorCode("用户注册失败")
    # 问题贴
    QUESTION_CREATE_FAILED = ErrorCode("问题贴创建失败")
    QUESTION_UPDATE_FAILED = ErrorCode("问题贴修改失败")

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

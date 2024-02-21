import re

from functools import wraps
from rest_framework import status
from rest_framework.response import Response


def is_valid_email(email):
    """判断是否为合法邮箱"""
    pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    return pattern.match(email)


def disable_actions(actions):
    """用于禁用指定的方法"""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(viewset, request, *args, **kwargs):
            if viewset.action in actions:
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
            return view_func(viewset, request, *args, **kwargs)
        return _wrapped_view
    return decorator

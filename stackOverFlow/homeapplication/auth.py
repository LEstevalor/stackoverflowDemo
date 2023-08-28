from django.contrib.auth.backends import ModelBackend


class MyAuthBackend(ModelBackend):
    """修改⽤户认证系统的后端，⽀持多账号登录"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        return request

import logging

from django.db.transaction import atomic
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.templatetags.rest_framework import data
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenViewBase
from blue_krill.web.drf_utils import inject_serializer

from stackOverFlow.homeapplication.error_codes import error_codes
from stackOverFlow.homeapplication.models import User
from stackOverFlow.homeapplication.serializers.users import (
    MyTokenObtainPairSerializer,
    CreateUserSerializer,
    UserSerializer
)

logger = logging.getLogger(__name__)


class LoginTokenView(TokenViewBase):
    """ jwt登录视图 按照TokenObtainPairView重写为自己调用的视图"""
    serializer_class = MyTokenObtainPairSerializer


class RegisterUserView(CreateAPIView):
    """用户注册视图"""
    serializer_class = CreateUserSerializer


class UserViewSet(GenericViewSet):
    """用户注册视图"""
    queryset = User.objects.filter()
    serializer_class = UserSerializer

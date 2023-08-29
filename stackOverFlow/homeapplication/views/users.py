import logging

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenViewBase

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


class UniqueView(APIView):
    """唯一注册视图"""
    def get(self, request):
        str = request.GET.get("str")
        front_str = request.GET.get(str)
        if str == "username":  # 检查是否有重复的账号
            # SQL: select count(*) from user where username = front_str
            count = User.objects.filter(username=front_str).count()
        else:  # 检查是否有重复的邮箱
            # SQL: select count(*) from user where email = front_str
            count = User.objects.filter(email=front_str).count()
        return Response({"count": count})


class RealNameView(APIView):
    """用户信息视图"""
    def get(self, request):
        username = request.GET.get("username")
        username = User.objects.get(username=username)
        if username is not None:
            return Response({'message': username}, status=status.HTTP_200_OK)
        return Response({'message': 'username错误'}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(GenericViewSet):
    """用户注册视图"""
    queryset = User.objects.filter()
    serializer_class = UserSerializer



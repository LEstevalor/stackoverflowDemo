import logging
from random import randint

from django.db.transaction import atomic
from django_redis import get_redis_connection
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenViewBase

from homeapplication.error_codes import error_codes
from homeapplication.models import User
from homeapplication.serializers.users import (
    MyTokenObtainPairSerializer,
    CreateUserSerializer,
    UserSerializer, UserDetailSerializer
)
from homeapplication.utils import is_valid_email

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
        """注册"""
        str = request.GET.get("str")
        front_str = request.GET.get(str)
        if str == "username":  # 检查是否有重复的账号
            # SQL: select count(*) from user where username = front_str
            count = User.objects.filter(username=front_str).count()
        else:  # 检查是否有重复的邮箱
            # SQL: select count(*) from user where email = front_str
            count = User.objects.filter(email=front_str).count()
        return Response({"count": count})

    def post(self, request):
        """重置密码"""
        username = request.data["username"]
        password = request.data["password"]
        email = request.data["email"]
        user = User.objects.filter(username=username, password=password, email=email).first()
        if not user:
            return Response({"message": "原密码不对"}, status=status.HTTP_400_BAD_REQUEST)

        password2 = request.data["password2"]
        password22 = request.data["password22"]
        if password2 != password22 or len(password2) < 6:
            return Response({"新密码重输不一致或密码小于6位"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user.password = password2
            user.save()
        except Exception:
            return Response({"重置密码失败"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class RealNameView(APIView):
    """用户信息视图"""
    def get(self, request):
        try:
            username = request.GET.get("username")
            username = User.objects.get(username=username).username
            if username:
                return Response({'message': username}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'message': 'username错误'}, status=status.HTTP_400_BAD_REQUEST)


class UserView(RetrieveAPIView):
    """⽤户登录信息鉴定"""
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    # 重写get_object方法返回给前端字段，否则会报queryset的错误
    def get_object(self):
        return self.request.user


class UserViewSet(GenericViewSet):
    """用户注册视图"""
    queryset = User.objects.filter()
    serializer_class = UserSerializer

    @atomic
    @swagger_auto_schema(
        tags=["用户 User"],
        operation_summary="发送验证码"
    )
    @action(detail=False, methods=["GET"])
    def email_send(self, request, *args, **kwargs):
        """通过用户邮箱，发送验证码，有效期为5分钟，存入非关系型数据库redis中"""
        email = request.GET.get("email")
        if not is_valid_email(email):
            return Response({'message': '邮箱格式不合法'}, status=status.HTTP_400_BAD_REQUEST)

        redis_conn = get_redis_connection('verify_codes')
        sms_code = "%06d" % randint(0, 999999)  # 自定义生成六位验证码
        send_flag = redis_conn.get('send_flag_%s' % email)
        if send_flag:
            return Response({'message': '频繁发送邮箱申请验证码'}, status=status.HTTP_400_BAD_REQUEST)
        print(sms_code)  # 生成环境中不留该类测试数据
        logger.info(sms_code)

        try:
            User.objects.email_send(redis_conn=redis_conn, email=email, sms_code=sms_code)
        except Exception:
            logger.exception("邮箱发送失败")
            raise error_codes.SENR_EMAIL_FAILED
        return Response({'message': 'ok'})

    @atomic
    @swagger_auto_schema(
        tags=["用户 User"],
        operation_summary="邮箱验证码验证"
    )
    @action(detail=False, methods=["GET"])
    def email_verify(self, request):
        """邮箱验证码验证"""
        try:
            # post请求 print(request.data)  # 测试数据：{'sms_code': 123456}
            front_email_code = request.GET.get("sms_code")  # 前端提交的验证码
            redis_conn = get_redis_connection('verify_codes')
            real_email_code = redis_conn.get('send_%s' % request.GET.get("email")).decode('UTF-8')
            # b'xxxxxx' bytes类型，需转成字符串，如果先转成int那么避免不了前面为0的情况，012345 -》 12345，字节型变字符串用bytes.decode('UTF-8')
        except Exception:
            logger.exception("邮箱验证有误")
            raise error_codes.EMAIL_VERIFY_FAILED

        if real_email_code is None:  # 验证码过期的情况
            return Response({'message': '验证码过期或未申请过'}, status=status.HTTP_400_BAD_REQUEST)
        if front_email_code != real_email_code:
            return Response({'message': '验证码错误'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'ok'}, status=status.HTTP_200_OK)

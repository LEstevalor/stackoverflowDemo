import re

from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from stackOverFlow.homeapplication.models import User


class MyTokenObtainPairSerializer(TokenObtainSerializer):
    """jwt序列化器"""
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        data['token'] = data['access']
        data['username'] = self.user.usernamera
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class CreateUserSerializer(serializers.ModelSerializer):
    """注册序列化器"""
    password2 = serializers.CharField(label='确认密码', write_only=True, required=False)
    token = serializers.CharField(label='token', read_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'token']

    def validate(self, attrs):
        """校验两个密码是否相同与校验邮箱"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('两个密码不一致')
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', attrs['email']):
            raise serializers.ValidationError('邮箱格式有误')
        return attrs

    @atomic
    def create(self, validated_data):
        del validated_data['password2']
        user = User(**validated_data)
        user.save()
        # 生成jwt
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)  # jwt载荷
        token = jwt_encode_handler(payload)  # 如果配置文件有SECRET_KEY，就只需传载荷，就能生成JWT
        user.token = token  # token返前端
        return user

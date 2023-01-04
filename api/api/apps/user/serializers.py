from rest_framework import serializers
from .models import User
from .utils import get_user_by_account
from django.contrib.auth.hashers import make_password
from rest_framework_jwt.settings import api_settings


class UserModelSerializer(serializers.ModelSerializer):
    """
    用户信息序列化器
    """
    token = serializers.CharField(max_length=1000, read_only=True, help_text="token认证字符串")

    class Meta:
        model = User
        fields = ["id", "username", "password", "token", "stated", "is_active"]
        extra_kwargs = {
            "id": {
                "read_only": True,
            },
            "password": {
                "write_only": True,
            }
        }

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        stated = attrs.get("stated")
        is_active = attrs.get("is_active")

        # 验证码用户名是否已经被注册过了
        ret = get_user_by_account(username)
        if ret is not None:
            raise serializers.ValidationError("对不起，该用户名已经被注册")

        return attrs

    def create(self, validated_data):
        """创建用户信息"""
        stated = validated_data.get("stated")
        activate = validated_data.get("is_active")
        # 加密密码
        raw_password = validated_data.get("password")
        hash_password = make_password(raw_password)
        # 设置用户名默认值
        username = validated_data.get("username")
        # 调用序列化器提供的create方法
        user = User.objects.create(
            username=username,
            password=hash_password,
            stated=stated,
            is_active=activate,
        )

        # 手动生成token的方法生成登录状态
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)

        return user


class UserInfoSerializer(serializers.ModelSerializer):
    """
    用户信息序列化器
    """

    class Meta:
        model = User
        fields = '__all__'


class UserRepairSerializer(serializers.ModelSerializer):
    """
    用户报修信息序列化器
    """

    class Meta:
        model = User
        fields = ['build_num', 'mobile', 'rom_num']


class UserParkingSerializer(serializers.ModelSerializer):
    """
    用户停车位信息序列化器
    """

    class Meta:
        model = User
        fields = ['id', 'build_num', 'mobile', 'car_num']

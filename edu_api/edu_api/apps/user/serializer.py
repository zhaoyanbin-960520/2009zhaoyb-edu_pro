import re

from django.contrib.auth.hashers import make_password
from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from user.models import UserInfo
from user.utils import get_user_by_account


class UserModelSerializer(ModelSerializer):
    token = serializers.CharField(max_length=1024, read_only=True, help_text="用户token")
    code = serializers.CharField(max_length=6, write_only=True, help_text='短信验证码')

    class Meta:
        model = UserInfo
        fields = ["phone", "password", "username", "token", "id", "code"]
        extra_kwargs = {
            "password": {
                "write_only": True,
            },
            "phone": {
                "write_only": True,
            },
            "username": {
                "read_only": True,
            },
            "id": {
                "read_only": True,
            },
        }

    def validate(self, attrs):
        """验证手机号与密码"""
        phone = attrs.get("phone")
        # print(len(phone))
        password = attrs.get("password")
        code = attrs.get('code')
        # print(len(password))
        # print(123)

        if not re.match(r'^1[3-9]\d{9}$', phone):
            raise serializers.ValidationError('手机号格式不正确')

        redis_connection = get_redis_connection('sms_code')
        phone_code = redis_connection.get("exp_%s" % phone)
        if phone_code.decode() != code:
            # 为了防止暴力破解，可以设置一个手机号只能验证n次  累加器
            raise serializers.ValidationError("验证码输入错误")
        if not re.match(r'^(?![0-9]+$)(?![a-z]+$)(?![A-Z]+$)(?!([^(0-9a-zA-Z)])+$).{8,16}$', password):
            raise serializers.ValidationError('密码格式不正确,密码格式为包含数字, 英文, 字符中的两种以上，且长度为8-16')

        # 验证手机号是否被注册
        try:
            user = get_user_by_account(phone)
        except UserInfo.DoesNotExist:
            user = None

        if user:
            raise serializers.ValidationError('当前手机号已经被注册')

        return attrs

    def create(self, validated_data):
        """重写保存对象的方法  完成用户信息的设置"""
        # 获取密码 进行加密处理
        # print(999)
        password = validated_data.get("password")
        # print(8888, password)
        hash_pwd = make_password(password)  # 加密后的密码

        # 对用户名进行设置默认值 手机号  随机字符串
        username = validated_data.get('phone')

        # 添加数据
        user_obj = UserInfo.objects.create(
            phone=username,
            username=username,
            password=hash_pwd,
            email=username + '@163.com'
        )

        # 为注册成功的用户生成token
        from rest_framework_jwt.settings import api_settings

        # 根据用户生成载荷
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER

        # 根据载荷生成token
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user_obj)
        user_obj.token = jwt_encode_handler(payload)

        return user_obj

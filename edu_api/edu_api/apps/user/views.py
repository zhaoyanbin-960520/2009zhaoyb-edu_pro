import random

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status as http_status
from rest_framework.generics import CreateAPIView
from django_redis import get_redis_connection

from edu_api.libs.geetest import GeetestLib
from edu_api.settings import constants
from edu_api.utils.send_message import Message
from user.models import UserInfo
from user.serializer import UserModelSerializer
from user.utils import get_user_by_account

pc_geetest_id = "45dbe199c830b4b9cb1bebd76fbbfdb7"
pc_geetest_key = "cbdff4cfb81c08cb1312f36b963fec22"


# 获取验证码视图函数
class CaptchaAPIView(APIView):
    """极验验证码"""

    user_id = 0
    status = False

    def get(self, request, *args, **kwargs):
        """获取验证码"""

        # 根据用户名验证当前用户是否存在
        account = request.query_params.get("username")
        # print(1)
        user = get_user_by_account(account)
        # print(2)

        if user is None:
            return Response({"message": "用户不存在"}, status=http_status.HTTP_400_BAD_REQUEST)

        self.user_id = user.id
        # print(3)

        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        self.status = gt.pre_process(self.user_id)
        # print(4)
        response_str = gt.get_response_str()
        return Response(response_str)

    def post(self, request, *args, **kwargs):
        """校验验证码"""

        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.data.get("geetest_challenge", '')
        validate = request.data.get("geetest_validate", '')
        seccode = request.data.get("geetest_seccode", '')
        account = request.data.get('username')
        user = get_user_by_account(account)

        if user:
            # 验证结果是否正确
            result = gt.success_validate(challenge, validate, seccode, self.user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        result = {"status": "success"} if result else {"status": "fail"}
        return Response(result)


# 用户注册视图函数
class UserAPIView(CreateAPIView):
    """用户注册"""
    queryset = UserInfo.objects.all()
    serializer_class = UserModelSerializer


class Checkphone(APIView):
    def get(self, request, *args, **kwargs):
        phone = kwargs.get("phone")
        try:
            UserInfo.objects.get(phone=phone)
            return Response("1")
        except:
            return Response("2")


class MessageAPIView(APIView):

    def get(self, request, *args, **kwargs):
        """
        获取验证码  为手机号生成验证码并发送
        :param request:
        """
        phone = request.query_params.get("phone")

        # 判断手机号是否在60s内发送过短信
        redis_connection = get_redis_connection("sms_code")
        mobile = redis_connection.get("sms_%s" % phone)

        if mobile is not None:
            return Response({"message": "您已经在60s内发送过短信了"},
                            status=http_status.HTTP_400_BAD_REQUEST)

        # 为当前手机号生成随机验证码  6位验证码
        code = "%06d" % random.randint(100000, 999999)

        # 将验证码保存到redis中
        # 验证码发送的间隔时间
        redis_connection.setex("sms_%s" % phone, constants.SMS_EXPIRE_TIME, code)
        # 保存验证的有效时间
        redis_connection.setex("exp_%s" % phone, constants.MOBILE_EXPIRE_TIME, code)

        # 调用方法  完成短信发送
        try:
            message = Message(constants.API_KEY)
            message.send_message(phone, code)
        except:
            return Response({"message": "短信发送失败，请稍后再试"},
                            status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 将发送结果响应到前端
        return Response({"message": "发送短信成功"}, status=http_status.HTTP_200_OK)

from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from user import views

urlpatterns = [
    # 借助于jwt完成登录请求
    path('login/', obtain_jwt_token),
    # 登录请求获取滑块验证码视图函数
    path("captcha/", views.CaptchaAPIView.as_view()),
    # 注册请求视图函数
    path("users/", views.UserAPIView.as_view()),
    # 注册获取短信验证码视图函数
    path("message/", views.MessageAPIView.as_view()),
    # 注册失焦验证手机号
    path('checkphone/<str:phone>', views.Checkphone.as_view())
]

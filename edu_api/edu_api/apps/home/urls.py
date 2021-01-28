from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from home import views

urlpatterns=[
    #轮播图视图
    path('img/',views.BannerAPIView.as_view()),
    #导航栏视图
    path('nav/',views.NavAPIView.as_view()),

]
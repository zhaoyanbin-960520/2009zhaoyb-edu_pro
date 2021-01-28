from rest_framework.generics import ListAPIView

from home.models import Banner, Nav
from home.serializer import BannerModelSerializer, NavModelSerializer


# 轮播图视图
class BannerAPIView(ListAPIView):
    queryset = Banner.objects.filter(is_show=True, is_delete=False).order_by('-orders')
    serializer_class = BannerModelSerializer


# 导航栏视图
class NavAPIView(ListAPIView):
    queryset = Nav.objects.filter(is_show=True, is_delete=False).order_by('-orders')
    serializer_class = NavModelSerializer

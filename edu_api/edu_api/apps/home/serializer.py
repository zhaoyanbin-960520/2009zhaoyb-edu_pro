from rest_framework.serializers import ModelSerializer

from home.models import Banner, Nav


class BannerModelSerializer(ModelSerializer):
    class Meta:
        model = Banner
        fields = ["img", "link"]


class NavModelSerializer(ModelSerializer):
    class Meta:
        model=Nav
        fields=['title','link','position','is_site']
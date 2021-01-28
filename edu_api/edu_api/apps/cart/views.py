from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from django_redis import get_redis_connection
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from course.models import Course
from edu_api.settings.constants import IMG_SRC


class CartViewSet(ViewSet):
    """购物车视图"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def add_cart(self, request):
        course_id = request.data.get('course_id')
        user_id = request.user.id
        print(user_id)
        select = True
        expire = 0

        try:
            Course.objects.get(is_show=True, is_delete=False, pk=course_id)
        except Course.DoesNotExist:
            return Response({'message': "参数有误，课程不存在"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            redis_connection = get_redis_connection('cart')

            pipeline = redis_connection.pipeline()

            pipeline.multi()
            pipeline.hset("cart_%s" % user_id, course_id, expire)
            pipeline.sadd("selected_%s" % user_id, course_id)

            pipeline.execute()

            cart_len = redis_connection.hlen('cart_%s' % user_id)
        except:
            return Response({'message': "参数有误，购物车添加失败"},
                            status=status.HTTP_507_INSUFFICIENT_STORAGE)

        return Response({'message': "购物车添加成功", 'cart_length': cart_len},
                        status=status.HTTP_200_OK)

    def list_cart(self, request):
        user_id = request.user.id
        redis_connection = get_redis_connection("cart")
        cart_list_byte = redis_connection.hgetall("cart_%s" % user_id)
        select_list_byte = redis_connection.smembers("selected_%s" % user_id)
        # print(123)
        data = []

        for course_id_byte, expire_id_byte in cart_list_byte.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)
            # print(666)

            try:
                course = Course.objects.get(is_delete=False, is_show=True, pk=course_id)
            except Course.DoesNotExist:
                continue

            data.append({
                "selected": True if course_id_byte in select_list_byte else False,
                "course_img": IMG_SRC + course.course_img.url,
                "name": course.name,
                "id": course.id,
                "expire_id": expire_id,
                "price": course.price

            })

        return Response(data)


class CartChangeViewSet(ViewSet):
    # 选中状态
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def change_selected(self, request):
        selected = request.data.get('selected')
        # print(123)
        course_id = request.data.get("course_id")
        # print(456)
        user_id = request.user.id
        # print(789)

        redis_connection = get_redis_connection("cart")

        if selected:
            redis_connection.sadd("selected_%s" % user_id, course_id)
        else:
            redis_connection.srem("selected_%s" % user_id, course_id)

        return Response(1)

    def del_cart(self, request):
        course_id = request.data.get("course_id")
        user_id = request.user.id
        redis_connection = get_redis_connection("cart")
        redis_connection.srem("selected_%s" % user_id, course_id)
        redis_connection.hdel("cart_%s" % user_id, course_id)

        return Response({"msg": "删除成功"})

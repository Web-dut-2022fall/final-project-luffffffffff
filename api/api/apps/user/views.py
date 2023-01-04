from django.db.models import Q
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .utils import save
from .paginations import UserPagination
from .serializers import UserModelSerializer, UserInfoSerializer
from .models import User
import json


# Create your views here.


class UserAPIView(CreateAPIView):
    """用户信息视图"""
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


class UserListAPIView(ListAPIView):
    """
    住户管理视图
    """
    queryset = User.objects.filter(stated=1).order_by('id')
    serializer_class = UserInfoSerializer
    # 分页
    pagination_class = UserPagination


class UserSearchAPIView(APIView):
    """
    搜索用户视图
    """

    def post(self, request):
        key_word = request.data.get('key')
        if key_word == '':
            res = User.objects.all()
        else:
            res = User.objects.filter(Q(first_name=key_word[0]) & Q(last_name=key_word[1:]))
        return Response(res.values())


class SaveAPIView(ViewSet):
    """
    用户个人信息视图
    """

    def add(self, request):
        # 保存用户个人信息
        data = request.data.get('info')
        uid = request.data.get('uid')
        user = User.objects.get(id=uid)
        if len(request.data) == 2:
            data['car_num'] = data['carnum1'] + data['carnum2']
            data.pop('carnum1')
            data.pop('carnum2')
        else:
            information = data
            flag = request.data.get('flag')
            data = save(flag, information)
        users = UserInfoSerializer()
        users.update(instance=user, validated_data=data)
        return Response({'msg': 'ok'})

    def show(self, request):
        # 获取用户个人信息
        uid = request.data.get('uid')
        user = User.objects.get(id=uid)
        users = []
        try:
            user_info = UserInfoSerializer(user, many=False)
            users = user_info.data
        except ValueError:
            Response({'msg': '获取用户信息失败'})
        return Response(users)

    def del_user(self, request):
        """
        删除用户
        """
        uid = request.query_params.get("uid")
        try:
            User.objects.get(id=uid)
        except User.DoesNotExist:
            return Response({"msg": "参数有误！当前用户不存在！"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=uid)
        user.delete()
        length = len(User.objects.all())
        return Response({"msg": "删除用户成功！", "length": length})

    def change_user(self, request):
        """
        修改用户信息
        """
        data = json.loads(request.body)
        print(data)
        uid = data.get('uid')
        if data.get('is_active'):
            data['is_active'] = 1
        else:
            data['is_active'] = 0
        if data.get('is_superuser'):
            data['is_superuser'] = 1
        else:
            data['is_superuser'] = 0
        if data.get('stated'):
            data['stated'] = 0
        else:
            data['stated'] = 1
        if data.get('sex') == '0':
            data['sex'] = '男'
        else:
            data['sex'] = '女'
        user = User.objects.get(id=uid)
        users = UserInfoSerializer()
        users.update(instance=user, validated_data=data)
        return Response({'msg': '修改成功'})

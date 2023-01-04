from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from .serializers import BuildingSerializer, HouseSerializer
from .models import Building, House
from .paginations import BuildPagination


# Create your views here.
class BuildListAPIView(ListAPIView):
    """
    楼栋管理视图
    """
    queryset = Building.objects.filter().order_by('id')
    serializer_class = BuildingSerializer
    # 分页
    pagination_class = BuildPagination


class HouseAPIView(ListAPIView):
    """
    住房管理视图
    """
    queryset = House.objects.filter().order_by('id')
    serializer_class = HouseSerializer
    # 分页
    pagination_class = BuildPagination


class BuildList(ListAPIView):
    """
    获取楼栋列表
    """
    queryset = Building.objects.filter(stated__gt=0).order_by('id')
    serializer_class = BuildingSerializer


class BuildSearchAPIView(APIView):
    """
    搜索楼栋视图
    """

    def post(self, request):
        key_word = request.data.get('key')
        print(key_word)
        if key_word == '':
            res = Building.objects.all()
        else:
            res = Building.objects.filter(name=key_word)
        return Response(res.values())


class HouseSearchAPIView(APIView):
    """
    搜索住房视图
    """

    def post(self, request):
        key_word = request.data.get('key')
        print(key_word)
        if key_word == '':
            res = House.objects.all()
        else:
            res = House.objects.filter(household=key_word)
        return Response(res.values())


class BuildManageViewSet(ViewSet):
    """
    楼栋操作视图
    """

    def add(self, request):
        data = request.data.get('info')
        builds = BuildingSerializer(data=data)
        if builds.is_valid():
            builds.save()
            return Response({'msg': 'ok'})
        else:
            return Response({'msg', '添加失败'})

    def show(self, request):
        # 获取楼栋信息
        bid = request.data.get('bid')
        build = Building.objects.get(id=bid)
        builds = []
        try:
            build_info = BuildingSerializer(build, many=False)
            builds = build_info.data
        except ValueError:
            Response({'msg': '获取楼栋信息失败'})
        return Response(builds)

    def del_build(self, request):
        """
        删除楼栋
        """
        bid = request.query_params.get("bid")
        try:
            Building.objects.get(id=bid)
        except Building.DoesNotExist:
            return Response({"msg": "参数有误！当前楼栋不存在！"}, status=status.HTTP_400_BAD_REQUEST)
        build = Building.objects.get(id=bid)
        build.delete()
        length = len(Building.objects.all())
        return Response({"msg": "删除楼栋成功！", "length": length})

    def change_build(self, request):
        """
        修改楼栋信息
        """

        data = request.data.get('data')
        if data['stated']:
            data['stated'] = 1
        else:
            data['stated'] = 0
        bid = request.data.get('bid')
        build = Building.objects.get(id=bid)
        builds = BuildingSerializer()
        builds.update(instance=build, validated_data=data)
        return Response({'msg': '修改成功'})


class HouseManageViewSet(ViewSet):
    """
    住房操作视图
    """

    def add(self, request):
        data = request.data.get('info')
        data['house_type'] = request.data.get('house_type')
        data['uni'] = request.data.get('uni')
        data['building'] = request.data.get('building')
        print(data)
        houses = HouseSerializer(data=data)
        if houses.is_valid():
            houses.save()
            return Response({'msg': '添加住房成功'})
        else:
            return Response({'msg', '添加住房失败'})

    def del_house(self, request):
        """
        删除住房
        """
        hid = request.query_params.get("hid")
        try:
            House.objects.get(id=hid)
        except House.DoesNotExist:
            return Response({"msg": "参数有误！当前住房不存在！"}, status=status.HTTP_400_BAD_REQUEST)
        house = House.objects.get(id=hid)
        house.delete()
        length = len(House.objects.all())
        return Response({"msg": "删除住房成功！", "length": length})

    def show(self, request):
        # 获取住房信息
        hid = request.data.get('hid')
        house = House.objects.get(id=hid)
        houses = []
        try:
            house_info = HouseSerializer(house, many=False)
            houses = house_info.data
        except ValueError:
            Response({'msg': '获取住房信息失败'})
        return Response(houses)

    def change_house(self, request):
        """
        修改住房信息
        """

        data = request.data.get('data')
        if data['stated']:
            data['stated'] = 1
        else:
            data['stated'] = 0
        hid = request.data.get('hid')
        house = House.objects.get(id=hid)
        houses = HouseSerializer()
        houses.update(instance=house, validated_data=data)
        return Response({'msg': '修改成功'})

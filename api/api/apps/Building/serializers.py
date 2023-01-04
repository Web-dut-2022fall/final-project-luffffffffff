from rest_framework import serializers
from .models import Building, House


class BuildingSerializer(serializers.ModelSerializer):
    """
    小区信息序列化器
    """

    class Meta:
        model = Building
        fields = '__all__'


class HouseSerializer(serializers.ModelSerializer):
    """
    住房信息序列化器
    """

    class Meta:
        model = House
        fields = '__all__'

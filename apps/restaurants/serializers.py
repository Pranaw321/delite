# import serializer from rest_framework
from rest_framework import serializers
from datetime import datetime
from .models import Restaurant
from ..menus.serializers import CategorySerializer


class RestaurantSerializer(serializers.ModelSerializer):
    category = CategorySerializer(source="category_set", many=True)

    class Meta:
        model = Restaurant
        fields = '__all__'
        depth = 1

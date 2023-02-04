# import serializer from rest_framework
from rest_framework import serializers
from datetime import datetime
from .models import Restaurant
from ..users.serializers import UserSerializer


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = '__all__'
        depth = 1

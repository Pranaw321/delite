# import serializer from rest_framework
from rest_framework import serializers
from datetime import datetime
from .models import Restaurant
from ..menus.serializers import CategorySerializer
from ..users.serializers import UserSerializer


class RestaurantSerializer(serializers.ModelSerializer):
    users = UserSerializer(source="restaurant_name", many=True)

    class Meta:
        model = Restaurant
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RestaurantSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            del self.fields['users']
        else:
            self.Meta.depth = 1



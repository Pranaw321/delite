# import serializer from rest_framework
from rest_framework import serializers
from .models import Item, Quantity, Category, AddsOn
# from ..restaurants.serializers import RestaurantSerializer
# from ..restaurants.serializers import RestaurantSerializer


class QuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Quantity
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    quantity = QuantitySerializer(source="quantity_set", many=True)

    class Meta:
        model = Item
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ItemSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            del self.fields['quantity']
        else:
            self.Meta.depth = 1


class AddsOnSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddsOn
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    item = ItemSerializer(source="item_category", many=True)
    # restaurant = RestaurantSerializer()

    class Meta:
        model = Category
        fields = ('name', 'desc', 'restaurant', 'status', 'item')
        read_only_fields = ['item']

    def __init__(self, *args, **kwargs):
        super(CategorySerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            del self.fields['item']
        else:
            self.Meta.depth = 1

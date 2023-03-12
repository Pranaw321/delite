import copy

from django.db.models import Prefetch, Count, prefetch_related_objects
from django.db.models.query_utils import Q
from rest_framework import viewsets

# import local data
from utils.helper import upload_image, unique_file_name
from .serializers import ItemSerializer, CategorySerializer, QuantitySerializer
from .models import Item, Category, Quantity

from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.settings import api_settings
from django.shortcuts import get_object_or_404

from .swagger import restaurant_prefix, restaurant_id, category_id
from ..restaurants.models import Restaurant


class CategoryViewSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin,
                      mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    # 1. List all
    def retrieve(self, request, pk=None):
        category = Category.objects.get(pk=pk)
        items = Category.objects.get(pk=pk).item_category.all().values()

        serializer = CategorySerializer(category)
        new_dict = copy.deepcopy(serializer.data)
        # new_dict['items'] = items
        return Response(new_dict)

    # 2. Create
    def create(self, request, *args, **kwargs):
        serializer = CategorySerializer(context={'request': request}, data=request.data)
        img = request.FILES["img"]
        if serializer.is_valid():
            filename = unique_file_name(request.FILES['img'].name)
            upload_image(filename, img)
            serializer.save(img=filename, restaurant_id=int(request.data.get('restaurant')))
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[restaurant_id, restaurant_prefix])
    def list(self, request):

        filters = {}
        if self.request.query_params.get('restaurant_prefix'):
            restaurant = Restaurant.objects.get(prefix=self.request.query_params.get('restaurant_prefix'))
            filters['restaurant_id'] = restaurant.id
        if self.request.query_params.get('restaurant_id'):
            filters['restaurant_id'] = self.request.query_params.get('restaurant_id')
        filter_q = Q(**filters)

        queryset = Category.objects.filter(filter_q)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CategorySerializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)


class ItemViewSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    # 1. List all
    def retrieve(self, request, pk=None):
        queryset = Item.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ItemSerializer(context={'request': request}, data=request.data)
        img = request.FILES["img"]
        if serializer.is_valid():
            filename = unique_file_name(request.FILES['img'].name)
            upload_image(filename, img)
            serializer.save(img=filename, restaurant_id=request.data.get('restaurant'),
                            category_id=request.data.get('category'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST', 'GET', 'PUT', 'DELETE'])
    def quantity(self, request, *args, **kwargs):
        if request and request.method == 'POST':
            serializer = QuantitySerializer(data=eval(request.data['quantity']), many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request and request.method == 'GET':
            filters = {}
            if self.request.query_params.get('item_id'):
                filters['item_id'] = self.request.query_params.get('item_id')
            filter_q = Q(**filters)
            quantity = Quantity.objects.filter(filter_q)
            serializer = QuantitySerializer(quantity, many=True)
            return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(manual_parameters=[restaurant_id, category_id])
    def list(self, request):
        # prepare filters to apply to queryset
        filters = {}
        if self.request.query_params.get('restaurant_id'):
            filters['restaurant_id'] = self.request.query_params.get('restaurant_id')
        if self.request.query_params.get('category_id'):
            filters['category_id'] = self.request.query_params.get('category_id')

        filter_q = Q(**filters)
        qs = Item.objects.prefetch_related(
            Prefetch('quantity_set', queryset=Quantity.objects.all())
        ).filter(filter_q)

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = ItemSerializer(qs, many=True)
            return self.get_paginated_response(serializer.data)

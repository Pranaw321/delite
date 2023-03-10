import copy
import json

from django.db.models import Prefetch, Count, prefetch_related_objects
from django.http import JsonResponse
from rest_framework import viewsets

# import local data
from .serializers import ItemSerializer, CategorySerializer, QuantitySerializer
from .models import Item, Category, Quantity
from ..users.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import mixins
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from mixin.myPaginationMixins import MyPaginationMixin
from rest_framework.settings import api_settings
from django.shortcuts import get_object_or_404
from utils.jwt.index import get_token_for_user, get_user_for_token
import jwt
from django.conf import settings

from ..users.serializers import UserSerializer


class CategoryViewSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin,
                      mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    # 1. List all
    def retrieve(self, request, pk=None):
        category = Category.objects.get(pk=pk)
        items = Category.objects.get(pk=pk).item_set.all().values()

        serializer = CategorySerializer(category)
        new_dict = copy.deepcopy(serializer.data)
        new_dict['items'] = items
        return Response(new_dict)

    # 2. Create
    def create(self, request, *args, **kwargs):
        serializer = CategorySerializer(context={'request': request}, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = Category.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CategorySerializer(queryset, many=True)
            # return Response(serializer.data, status=status.HTTP_200_OK)
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
        return Response(serializer)

    def create(self, request, *args, **kwargs):
        serializer = ItemSerializer(context={'request': request}, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST', 'GET', 'PUT'])
    def quantity(self, request, *args, **kwargs):
        if request and request.method == 'POST':
            serializer = QuantitySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request and request.method == 'GET':
            return Response({})

    def list(self, request):
        qs = Item.objects.prefetch_related(
            Prefetch('quantity_set', queryset=Quantity.objects.all())
        )

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = ItemSerializer(qs, many=True)
            return self.get_paginated_response(serializer.data)

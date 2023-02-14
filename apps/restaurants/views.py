# import viewsets
import copy

from django.db.models.query import QuerySet
from django.http import JsonResponse
from rest_framework.filters import BaseFilterBackend
import coreapi
from django.db.models import Prefetch
from rest_framework import viewsets

# import local data
from .serializers import RestaurantSerializer
from .models import Restaurant
from ..menus.models import Category, Item
from ..menus.serializers import CategorySerializer
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


class RestaurantViewSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]
    # lookup_field = "id"
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    # 1. List all
    def retrieve(self, request, pk=None):
        queryset = Restaurant.objects.all()

        restaurant = get_object_or_404(queryset, pk=pk)

        qs = Category.objects.prefetch_related(
            Prefetch('item_category', queryset=Item.objects.all())
        ).filter(pk=pk)

        serializer = RestaurantSerializer(restaurant)
        new_dict = copy.deepcopy(serializer.data)
        category_serializer = CategorySerializer(qs, many=True)
        new_dict['category'] = category_serializer.data

        return Response(new_dict)

    # 2. Create
    def create(self, request, *args, **kwargs):
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = Restaurant.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = RestaurantSerializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)

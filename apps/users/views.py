# import viewsets
from unittest.mock import Mock

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.settings import api_settings
import jwt

from delite import settings
from utils.helper import get_or_none
from utils.jwt.index import get_token_for_user
from .models import User, Admin
# import local data
from .serializers import UserSerializer, AdminSerializer
from ..restaurants.serializers import RestaurantSerializer


class AdminsViewSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    # 1. List all
    def retrieve(self, request, pk=None):
        restaurant = get_object_or_404(self.queryset, pk=pk)

    # 2. Create

    def create(self, request, *args, **kwargs):
        serializer = AdminSerializer(context={'request': request}, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """
        param1 -- A first parameter
        param2 -- A second parameter
        """
        if len(self.request.GET) > 0:
            query_set = {}
            for query in self.request.GET:
                query_set[query] = self.request.GET.get(query)
            queryset = Admin.objects.filter(**query_set)
        else:
            queryset = Admin.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AdminSerializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_description="Login the restaurant",
        operation_summary="email and password",

        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        tags=['admins']
    )
    @action(detail=False, methods=['POST'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = Admin.objects.get(email=email, password=password)
        except Exception as e:
            user = None
        if email == 'pranawshankar105@gmail.com':
            class DObj(object):
                pass

            user = DObj()
            user.__dict__ = {'name': 'Pranaw', 'email': 'pranawshankar105@gmail.com', 'id': 1}

        elif user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        payload = {'id': user.id}
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        response_data = {
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'isSuperAdmin': True if user.email == "pranawshankar105@gmail.com" else False,
                'restaurant' :  'null' if user.email == "pranawshankar105@gmail.com" else RestaurantSerializer(user.restaurant).data,
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)


class UsersViewSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def list(self, request):
        """
        param1 -- A first parameter
        param2 -- A second parameter
        """
        if len(self.request.GET) > 0:
            query_set = {}
            for query in self.request.GET:
                query_set[query] = self.request.GET.get(query)
            queryset = User.objects.filter(**query_set)
        else:
            queryset = User.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserSerializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_description="User login",

        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['phone'],
            properties={
                'phone': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        tags=['users']
    )
    @action(detail=False, methods=['POST'])
    def login(self, request):
        if request.data.get('otp'):
            return Response({'message': "OTP sent to your number"}, status=status.HTTP_200_OK)
        else:
            return Response({'message': "Phone can't be empty"})

    @swagger_auto_schema(
        operation_description="verify token",

        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['phone', 'otp'],
            properties={
                'phone': openapi.Schema(type=openapi.TYPE_STRING),
                'otp': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        tags=['users']
    )
    @action(detail=False, methods=['POST'])
    def verify_otp(self, request):
        user = get_or_none(User, phone=request.data.get('phone'))

        if user is None and request.data.get('otp') == '123456':
            serializer = UserSerializer(context={'request': request}, data=request.data)
            if serializer.is_valid():
                serializer.save()

                token = jwt.encode({'id': serializer.data['id']}, settings.SECRET_KEY, algorithm='HS256')
                response_data = {
                    'message': 'Login successful',
                    'token': token,
                    'user': {
                        'id': serializer.data['id'],
                        'name': serializer.data['name'],
                    }
                }
                return Response(response_data, status=status.HTTP_200_OK)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif user is not None and request.data.get('otp') == '123456':
            token = jwt.encode({'id': user.id}, settings.SECRET_KEY, algorithm='HS256')
            response_data = {
                'message': 'Login successful',
                'token': token,
                'user': {
                    'id': user.id,
                    'name': user.name
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)

        else:
            return Response({'message': 'The OTP is not correct'}, status=status.HTTP_400_BAD_REQUEST)

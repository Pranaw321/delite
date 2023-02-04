# import viewsets
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
from utils.jwt.index import get_token_for_user
from .models import User
# import local data
from .serializers import UserSerializer


class UsersViewSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin):
    # add permission to check if restaurant is authenticated
    # permission_classes = [permissions.IsAuthenticated]
    # lookup_field = "id"
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    # 1. List all
    def retrieve(self, request, pk=None):
        restaurant = get_object_or_404(self.queryset, pk=pk)

    # 2. Create

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(context={'request': request}, data=request.data)
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
            queryset = User.objects.filter(**query_set)
        else:
            queryset = User.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserSerializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_description="Login the restaurant",
        operation_summary="email and password",

        # request_body is used to specify parameters
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        tags=['users']
    )
    @action(detail=False, methods=['POST'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email, password=password)
        except Exception as e:
            user = None

        if user is None:
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
                'isSuperAdmin': True if user.email == "pranawshankar105@gmail.com" else False

            }
        }
        return Response(response_data, status=status.HTTP_200_OK)

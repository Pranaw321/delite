# basic URL Configurations
from django.urls import include, path


# import everything from views
from .views import *

from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'orders', OrderViewSet)
router.register(r'orders/item', OrderItemViewSet)


# specify URL Path for rest_framework
urlpatterns = [
    path('', include(router.urls)),
]

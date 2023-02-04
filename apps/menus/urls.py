# basic URL Configurations
from django.urls import include, path
# import routers
from rest_framework import routers

# import everything from views
from .views import *

from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'menu/items', ItemViewSet)
router.register(r'category', CategoryViewSet)

# specify URL Path for rest_framework
urlpatterns = [
    path('', include(router.urls)),
]

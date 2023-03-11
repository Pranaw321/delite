from drf_yasg import openapi

restaurant_prefix = openapi.Parameter('restaurant_prefix', openapi.IN_QUERY, required=True,
                                      description="Get category list by restaurant name/prefix",
                                      type=openapi.TYPE_STRING)

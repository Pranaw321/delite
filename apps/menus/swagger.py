from drf_yasg import openapi

restaurant_prefix = openapi.Parameter('restaurant_prefix', openapi.IN_QUERY, required=False,
                                    description="Get category list by restaurant name/prefix",
                                    type=openapi.TYPE_STRING)

restaurant_id = openapi.Parameter('restaurant_id', openapi.IN_QUERY, required=False,
                                      description="Get category list by restaurant",
                                      type=openapi.TYPE_NUMBER)


category_id = openapi.Parameter('category_id', openapi.IN_QUERY, required=False,
                                description="Get item list by category",
                                type=openapi.TYPE_NUMBER)
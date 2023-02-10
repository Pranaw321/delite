import json

from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request):
        if request.method == 'POST':
            serializer = OrderSerializer(data=request.data)
            order_items_data = json.loads(request.data.get('order_items'))
            order_items_serializer = OrderItemSerializer(data=order_items_data, many=True)
            if serializer.is_valid() and order_items_serializer.is_valid():
                order = serializer.save()
                order_items = order_items_serializer.validated_data
                for order_item in order_items:
                    order_item['order'] = order
                    OrderItem.objects.create(**order_item)
                    response = {
                        'order': serializer.data,
                        'order_items': order_items_serializer.data,
                    }
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

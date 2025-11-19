from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from order.models import Order
from order.api.serializer import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', 'get', 'delete', 'patch']
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        obj = Order.objects.all()
        return obj
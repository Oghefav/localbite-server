from rest_framework import serializers
from user.api.serializers import  CustomerSerializer
from order.models import Order

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    class Meta:
        model = Order
        fields = ['order_id', 'customer', 'status', 'total_price', 'created_at' ]
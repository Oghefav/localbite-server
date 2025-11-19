from rest_framework import serializers
from order.api.serializer import OrderSerializer    
from user.api.serializers import DriverSerializer
from delivery.models import Delivery

class DeliverySerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    driver = DriverSerializer(read_only=True)

    class Meta:
        model = Delivery
        fields = ['delivery_id', 'order', 'driver', 'address', 'driver_status', 'created_at', 'updated_at']
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from delivery.models import Delivery
from delivery.api.serializer import DeliverySerializer

class DeliveryViewSet(viewsets.ModelViewSet):
    serializer_class = DeliverySerializer
    permission_classes = [AllowAny]

    # Optional: filter by driver_status
    def get_queryset(self):
        obj = Delivery.objects.all()
        return obj
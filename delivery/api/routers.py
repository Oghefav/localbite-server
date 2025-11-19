from rest_framework import routers
from delivery.api.viewsets import DeliveryViewSet

router = routers.DefaultRouter()
router.register(r'delivery', DeliveryViewSet, basename='delivery')

urlpatterns = [
    *router.urls
]

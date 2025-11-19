from rest_framework import routers
from order.api.viewsets import OrderViewSet

router = routers.DefaultRouter()
router.register(r'order', OrderViewSet, basename='order')

urlpatterns = [
    *router.urls
    ]
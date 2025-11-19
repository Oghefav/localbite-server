from rest_framework import routers
from cart.api.viewset import CartViewSet, CartItemViewSet

router = routers.DefaultRouter()

router.register(r'cart', CartViewSet, basename='cart')
router.register(r'cart_item', CartItemViewSet, basename='cart_item')

urlpatterns = [
    *router.urls
]
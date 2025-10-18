from rest_framework import routers
from user.api.viewsets import CustomUserViewset, ChefViewset, DriverViewset, CustomerViewset

router = routers.DefaultRouter()

router.register(r'user', CustomUserViewset, basename='custom_user')
router.register(r'chef', ChefViewset, basename='chef')
router.register(r'customer', CustomerViewset, basename='customer')
router.register(r'driver', DriverViewset, basename='driver')

urlpatterns = [
    *router.urls
]
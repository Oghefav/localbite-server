from rest_framework import routers
from authentication.api.viewset import CustomerRegistrationViewset, ChefRegistrationViewSet, DriverRegisterViewSet, loginViewSet

router = routers.DefaultRouter()

router.register(r'customer_registration', CustomerRegistrationViewset, basename='CustomerRegistration')
router.register(r'chef_registration', ChefRegistrationViewSet, basename='ChefRegistration')
router.register(r'driver_registration', DriverRegisterViewSet, basename='DriverRegistration')
router.register(r'login', loginViewSet, basename='login')

urlpatterns = [
    *router.urls
]
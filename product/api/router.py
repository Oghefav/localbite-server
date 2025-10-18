from rest_framework import routers
from product.api.viewsets import MealViewset

router = routers.DefaultRouter()

router.register(r'meal', MealViewset, basename='meal')

urlpatterns = [
    *router.urls
]
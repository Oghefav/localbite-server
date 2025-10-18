from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from product.models import Meal
from product.api.serializers import MealSerializer

class MealViewset(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']  
    serializer_class = MealSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # remember to make it only food added 1 day
        obj = Meal.objects.all()
        return obj


    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
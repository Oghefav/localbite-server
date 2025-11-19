from rest_framework import serializers
from product.models import Meal
from user.api.serializers import ChefSerializer

class MealSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField( read_only=True)
    chef = ChefSerializer(read_only=True)
    created_at=serializers.DateTimeField(read_only=True)
    update_at =serializers.DateTimeField(read_only=True)


    class Meta:
        model = Meal
        fields = ['id', 'title', 'chef', 'units', 'description', 'price', 'image', 'avaliability_status','created_at', 'update_at']
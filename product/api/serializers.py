from rest_framework import serializers
from product.models import Meal

class MealSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField( read_only=True)
    chef = serializers.StringRelatedField(read_only=True)
    created_at=serializers.DateTimeField(read_only=True)
    update_at =serializers.DateTimeField(read_only=True)


    class Meta:
        model = Meal
        fields = ['id', 'title', 'chef', 'units', 'description', 'price', 'image', 'created_at', 'update_at']
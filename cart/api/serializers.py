from rest_framework import serializers
from cart.models import CartItem, Cart
from user.api.serializers import CustomerSerializer
from product.api.serializers import MealSerializer

class CartSerializer(serializers.ModelSerializer):
    cart_items = serializers.SerializerMethodField()
    cart_total = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['cart_code', 'customer', 'cart_items', 'cart_total']

    def get_cart_items(self, obj):
        objs = CartItem.objects.filter(cart=obj)
        return CartItemSerializer(objs, many=True).data
    
    def get_cart_total(self, cart):
        items = cart.cart_items.all()
        total = sum([item.meal.price * item.quantity for item in items])
        return total
    
class CartItemSerializer(serializers.ModelSerializer):
    meal = MealSerializer()
    class Meta:
        model = CartItem
        fields = ['cart', 'meal', 'quantity']

# class AddCartItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CartItem
#         fields = ['cart', 'meal', 'quantity']

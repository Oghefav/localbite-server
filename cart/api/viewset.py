from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework  import status
from rest_framework.permissions import AllowAny
from cart.api.serializers import CartSerializer, CartItemSerializer
from cart.models import Cart, CartItem
from rest_framework.decorators import action 
from product.models import Meal

class CartViewSet(viewsets.ModelViewSet) :
    http_methods_names = ['get', 'delete']
    serializer_class = CartSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        obj = Cart.objects.all()
        return obj
    
class CartItemViewSet(viewsets.ModelViewSet):
    http_methods_names = ['get', 'post', 'put', 'delete']
    serializer_class = CartItemSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        obj = CartItem.objects.all()
        return obj
    
    @action(detail=False, methods=['post'], url_path='add-to-cart')
    def add_to_cart(self, request,):
        try:
            meal_id = request.data.get('meal_id')
            quantity = request.data.get('quantity', 1)
            cart_code = request.data.get('cart_code')
            if not meal_id:
                return Response(
                    {'error': 'meal_id is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not cart_code:
                return Response(
                    {'error': 'cart_code is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart = Cart.objects.get(cart_code=cart_code)
            meal = Meal.objects.get(id=meal_id)
            try:
                cart_item = CartItem.objects.get(cart=cart, meal=meal)
                # If exists, update quantity
                cart_item.quantity += quantity
                cart_item.save()
                created = False
            except CartItem.DoesNotExist:
                # If doesn't exist, create new one
                cart_item = CartItem.objects.create(
                    cart=cart, 
                    meal=meal,
                    quantity=quantity
                )
                created = True
            serializer = self.serializer_class(cart_item)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


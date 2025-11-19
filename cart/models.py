from django.db import models
import secrets
import string
from product.models import Meal
from user.models import Customer
# Create your models here.

def generate_code():
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))
class Cart(models.Model):
    cart_code = models.CharField(max_length=6, default=generate_code, unique=True, primary_key=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return self.cart_code


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='cart_item')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return   f"{self.meal.title } {self.quantity}"


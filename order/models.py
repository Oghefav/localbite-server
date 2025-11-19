from django.db import models
import uuid
from user.models import Customer
from cart.models import Cart
# Create your models here.

class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'pending' , 'Pending'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'
    order_id = models.URLField(primary_key=True, editable=False, default= uuid.uuid4, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length= 10, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    total_price = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='orders', null=True) 

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order {self.order_id} - {self.customer.user.get_full_name()}"
    
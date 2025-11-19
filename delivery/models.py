from django.db import models
from user.models import Driver
from order.models import Order
import uuid
# Create your models here.
class Delivery(models.Model):
    class DriveryStatusChoices(models.TextChoices):
        NEW = 'new', 'New'
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'

    delivery_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery')
    driver = models.OneToOneField(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_delivery')
    address = models.CharField(max_length=255)
    driver_status = models.CharField(max_length=10, choices=DriveryStatusChoices.choices, default=DriveryStatusChoices.NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
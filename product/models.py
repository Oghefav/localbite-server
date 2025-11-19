import uuid
from django.db import models
from user.models import Chef

# Create your models here.

class Meal(models.Model):
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    title = models.CharField(max_length=50,)
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE)
    units = models.PositiveIntegerField()
    description = models.TextField()
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='meal_images',)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    update_at = models.DateTimeField(auto_now=True, null=True)
    avaliability_status = models.BooleanField(default=True, null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
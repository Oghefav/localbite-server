from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid
import re
# Create your models here.

enugu_lga_code = ['DBR', 'AWG', 'NKW', 'ENU', 'UWN', 'AGW', 'GBD', 'ENZ', 'BBG', 'KEM', 'MGL', 'AGN', 'NSK', 'JRV', 'BLF', 'UDD', 'UMU']

def validate_license_number(license_number):
    pattern = r'^[A-Z]{3}-\d{3}[A-Z]{2}$|^[A-Z]{2}\d{3}-[A-Z]{3}$'

    if not re.match(pattern, license_number):
        raise ValidationError('license number is invalid')
    
    parts = license_number.split('-') 
    if len(parts[0]) == 3:
        lga_code = parts[0]  #ABC-124DF
    else:
        lga_code = parts[1] #DF1234-ABC
    if lga_code not in enugu_lga_code:
        raise ValidationError('invalid license number')
    

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('User must have an email')
        if not password:
            raise ValueError('User must have a password')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('SuperUser must have an email')
        if not password:
            raise ValueError('SuperUser must have a password')
        
        user = self.create_user(email=email, password=password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    username = None
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True,)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        # return f"{self.first_name} {self.last_name}"
        return self.get_full_name()
    

class Chef(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='chef', primary_key=True)
    bio = models.TextField(null=True, blank= True)
    brand_image = models.ImageField(upload_to='brand_img', blank=True, null=True)
    brand_name = models.CharField(unique=True,max_length=50, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    account_number = models.BigIntegerField(null=True)
    account_name = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.brand_name

    
class Driver(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='driver', primary_key=True)
    license_number = models.CharField(max_length=10, unique=True, validators=[validate_license_number])
    account_number = models.BigIntegerField(null=True)
    account_name = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_available = models.BooleanField(default=True, null=True)
    def __str__(self):
        return f"{self.user.first_name} {self.license_number}"

class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='customer')
    address = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    



from django.contrib import admin
from user.models import CustomUser, Chef, Customer, Driver
# Register your models here.

admin.site.register([Customer, Chef, CustomUser, Driver])
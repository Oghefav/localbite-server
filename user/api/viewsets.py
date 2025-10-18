from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from user.models import Chef, CustomUser, Customer, Driver
from user.api.serializers import CustomerSerializer, CustomUserSerializer, DriverSerializer, ChefSerializer

class CustomUserViewset(viewsets.ModelViewSet):
    http_method_names = ['get', 'patch', 'destroy', ]
    serializer_class = CustomUserSerializer
    Permission_classes = [IsAuthenticated]
    

    def get_queryset(self):
        obj = CustomUser.objects.all()
        return obj

    def get_object(self):
        obj = get_object_or_404(CustomUser, id=self.kwargs['pk'])    
        return obj
        


class DriverViewset(viewsets.ModelViewSet):
    http_method_names = ['get', 'patch', 'destroy',]
    serializer_class = DriverSerializer
    Permission_classes = [IsAuthenticated]

    def get_queryset(self):
        obj = Driver.objects.all()
        return obj
    
    def get_object(self):
        obj = get_object_or_404(Driver, id=self.kwargs['pk'])
        return obj

class ChefViewset(viewsets.ModelViewSet):
    http_method_names = ['get', 'patch', 'destroy',]
    serializer_class = ChefSerializer
    Permission_classes = [IsAuthenticated]

    def get_queryset(self):
        obj = Chef.objects.all()
        return obj
    
    def get_object(self):
        obj = get_object_or_404(Chef, id=self.kwargs['pk'])
        return obj

class CustomerViewset(viewsets.ModelViewSet):
    http_method_names = ['get', 'patch', 'destroy',]
    serializer_class = CustomerSerializer
    Permission_classes = [IsAuthenticated]

    def get_queryset(self):
        obj = Customer.objects.all()
        return obj
    
    def get_object(self):
        obj = get_object_or_404(CustomUser, id=self.kwargs['pk'])
        return obj
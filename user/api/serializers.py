from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password as django_password_validator
from django.core.exceptions import ValidationError
from user.models import CustomUser, Chef, Driver, Customer

class CustomUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True)
    is_active = serializers.BooleanField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'email','first_name', 'last_name', 'phone_number', 'is_active', 'password', 'confirm_password']

    def validate_password(self, value):
        try:
            django_password_validator(value)
            print('i am here')
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value
    
    def validate(self, attrs):
        if attrs['confirm_password'] != attrs['password']:
            raise serializers.ValidationError('passwords do not match')
        return attrs

class CustomerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = Customer
        fields = ['user', 'address', ]

class DriverSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta: 
        model = Driver
        fields = ['user', 'license_number', 'account_number', 'account_name']

class ChefSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Chef
        fields = ['brand_name', 'brand_name', 'brand_image', 'bio', 'address', 'user', 'account_number', 'account_name']

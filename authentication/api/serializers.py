from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password as django_password_validator
from user.models import Customer, Chef, Driver, CustomUser
from user.api.serializers import CustomUserSerializer


class CustomerRegisterSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = Customer
        fields = ['user' , 'address']

    def create(self, validated_data):
        user = validated_data.pop('user')
        user.pop('confirm_password')
        user = CustomUser.objects.create_user(**user)
        return Customer.objects.create(user=user, address=validated_data['address'])
    
class ChefRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, source='user.password')
    is_active = serializers.BooleanField(read_only=True)
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    phone_number = serializers.CharField(source='user.phone_number')
    is_active= serializers.BooleanField(source='user.is_active',read_only=True)
    class Meta:
        model = Chef
        fields = [ 'email','first_name', 'last_name', 'phone_number', 'is_active', 'password', 'confirm_password','bio', 'brand_image', 'brand_name', 'address']

    def create(self, validated_data):
            user_data = validated_data.pop('user')
            validated_data.pop('confirm_password')
            user = CustomUser.objects.create_user(**user_data)
            return Chef.objects.create(user=user, **validated_data)
        
    def validate_password(self, value):
        try:
            django_password_validator(value)
            print('i am here')
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value
    
    def validate(self, attrs):
        if attrs['confirm_password'] != attrs['user']['password']:
            raise serializers.ValidationError('passwords do not match')
        return attrs
    
class DriverRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, source='user.password')
    confirm_password =serializers.CharField(write_only=True)
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    phone_number = serializers.CharField(source='user.phone_number')

    class Meta:
        model = Driver
        fields = ['email', 'first_name', 'last_name', 'phone_number','license_number','confirm_password', 'password',]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(**user_data)
        return Driver.objects.create(user=user, **validated_data)

    def validate_password(self, value):
        try:
            django_password_validator(value)
            print('i am here')
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value
    
    def validate(self, attrs):
        if attrs['confirm_password'] != attrs['user']['password']:
            raise serializers.ValidationError('passwords do not match')
        return attrs
    

class DriverSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer
    class Meta:
        model = Driver
        fields = ['user', 'license_number']

class ChefSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer
    class Meta:
        model = Chef
        fields = ['user', 'bio', 'brand_image', 'brand_name', 'address']

class CustomerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer
    class Meta:
        model = Customer
        fields = ['user', 'address']


class LoginSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField(write_only=True)

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    
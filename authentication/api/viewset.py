from rest_framework import viewsets
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.permissions import AllowAny 
from rest_framework.authtoken.models import Token
from user.models import Chef, CustomUser, Driver, Customer
from user.api.serializers import ChefSerializer, DriverSerializer, CustomerSerializer
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.views import APIView
from authentication.api.serializers import CustomerRegisterSerializer, ChefRegisterSerializer, DriverRegisterSerializer, LoginSerializer, ResetPasswordSerializer
from cart.models import Cart

class CustomerRegistrationViewset(viewsets.ModelViewSet):
    http_method_names = ['post',]
    serializer_class = CustomerRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['user']['email']

        if CustomUser.objects.filter(email=email).exists():
            return Response({'message' : 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            user = CustomUser.objects.get(email = email)
            
            token = Token.objects.create(user=user)
            
            return Response({'message' : 'registration is successfull', 'token' : token.key, 'data' : serializer.data}, status=status.HTTP_201_CREATED) 


class ChefRegistrationViewSet(viewsets.ModelViewSet):
    http_method_names = ['post',]
    serializer_class = ChefRegisterSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, JSONParser]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['user']['email']
        brand_name = serializer.validated_data['brand_name']

        if CustomUser.objects.filter(email=email).exists():
            return Response({'message' : 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if Chef.objects.filter(brand_name=brand_name).exists():
            return Response({'message' : 'User with this brand already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            user = CustomUser.objects.get(email = email)
            token = Token.objects.create(user=user)
            return Response({'message' : 'registration is successfull', 'token' : token.key, 'data' : serializer.data}, status=status.HTTP_201_CREATED) 
        

class DriverRegisterViewSet(viewsets.ModelViewSet):
    http_method_names = ['post',]
    serializer_class = DriverRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['user']['email']
        license_number = serializer.validated_data['license_number']

        if CustomUser.objects.filter(email=email).exists():
            return Response({'message' : 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if Driver.objects.filter(license_number=license_number).exists():
            return Response({'message' : 'User with this driver license already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else: 
            serializer.save()
            user = CustomUser.objects.get(email = email)
            token = Token.objects.create(user=user)
            return Response({'message' : 'registration is successfull', 'token' : token.key, 'data' : serializer.data}, status=status.HTTP_201_CREATED)
        

class loginViewSet(viewsets.ViewSet):
    serializer_class = LoginSerializer
    http_method_names = ['post']
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer)
    def create(self, request): 
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, username=email, password=password)
        if user is None:
            return Response({'message' : 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        formal_token = Token.objects.filter(user=user)
        formal_token.delete()
        new_token = Token.objects.create(user=user)

        if Chef.objects.filter(user=user).exists():
            user_type = 'chef'
            chef = Chef.objects.get(user=user)
            user_serializer = ChefSerializer(chef)

        elif Driver.objects.filter(user=user).exists():
            user_type = 'driver'
            driver = Driver.objects.get(user=user)
            user_serializer = DriverSerializer(driver)

        elif Customer.objects.filter(user=user).exists():
            user_type = 'customer'
            customer = Customer.objects.get(user=user)
            cart_code = Cart.objects.get(customer=customer).cart_code
            user_serializer = CustomerSerializer(customer)
            return Response({'message' : 'login successful','user_type' : user_type ,'token' : new_token.key, 'cart_code': cart_code,'data' : user_serializer.data}, status=status.HTTP_200_OK)
        else:
            user_type = 'admin'

        
        return Response({'message' : 'login successful','user_type' : user_type ,'token' : new_token.key, 'data' : user_serializer.data}, status=status.HTTP_200_OK)


class ResetPassword(viewsets.ViewSet):
    http_method_names = ['post']
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        if not CustomUser.objects.filter(email=email).exists():
            return Response({'message' : 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # send email to the user with the reset link
            return Response({'message' : 'reset link is sent to your email'}, status=status.HTTP_200_OK)
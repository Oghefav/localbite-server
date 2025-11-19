from django.shortcuts import render

# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from localbite.utility.payment import Paystack
from user.models import Customer
from order.models import Order
from user.models import Driver

class InitPayView(APIView):
    @swagger_auto_schema(
        operation_description="Initialize Paystack payment",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'amount': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['email', 'amount'],
        ),
        responses={200: "Payment Initialized"},
    )
    def post(self, request):
        email = request.data.get("email")
        amount = request.data.get("amount")

        paystack = Paystack()
        callback = "https://yourdomain.com/api/payment/verify/"

        resp = paystack.initialize_payment(email, amount, callback)
        return Response(resp)


class VerifyPayView(APIView):
    @swagger_auto_schema(
        operation_description="Verify Paystack transaction",
        manual_parameters=[
            openapi.Parameter(
                'reference',
                openapi.IN_QUERY,
                description="Transaction reference",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={200: "Verification result"},
    )
    def get(self, request):
        reference = request.query_params.get("reference")
        if not reference:
            return Response({"error": "Reference is required"}, status=400)

        paystack = Paystack()
        resp = paystack.verify_payment(reference)

        if resp.get("data", {}).get("status") == "success":
            email = resp["data"]["customer"]["email"]
            customer = Customer.objects.get(user__email=email)
            
            # Get customer's active cart
            cart = customer.cart_set.filter(is_active=True).first()
            if not cart:
                return Response({"error": "No active cart found"}, status=400)

            total_amount = resp["data"]["amount"] // 100

            # Create Order from cart
            order = Order.objects.create(
                customer=customer,
                cart=cart,
                status=Order.StatusChoices.COMPLETED,
                total_price=total_amount
            )

            # Mark cart as inactive
            cart.is_active = False
            cart.save()

            # --- Notify chefs ---
            chefs = set()
            for item in cart.cart_items.all():  # iterate through CartItems
                meal = item.meal
                chefs.add(meal.chef)  # set ensures no duplicates

            for chef in chefs:
                send_notification(
                    user=chef.user,
                    title="New Order",
                    message=f"Order {order.order_id} has been placed including your meal(s)."
                )

            # --- Notify a single available driver ---
            driver = Driver.objects.filter(is_available=True).first()
            if driver:
                send_notification(
                    user=driver.user,
                    title="New Delivery",
                    message=f"Order {order.order_id} is ready for delivery."
                )

            return Response({
                "message": "Payment verified, order created, notifications sent",
                "order_id": str(order.order_id),
                "payment_status": "success"
            })

        return Response({
            "message": "Payment verification failed",
            "payment_status": resp.get("data", {}).get("status", "failed")
        })

from django.urls import path
from .views import InitPayView, VerifyPayView

urlpatterns = [
    path("payment/init/", InitPayView.as_view()),
    path("payment/verify/", VerifyPayView.as_view()),
]

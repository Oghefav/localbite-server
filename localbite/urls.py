"""
URL configuration for localbite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from localbite.schema import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/docs/', schema_view.with_ui('swagger',cache_timeout=0,), name='swagger-docs'),
    path('user/', include('user.api.router')),
    path('auth/', include('authentication.api.routers')),
    path('meal/', include('product.api.router')),
    path('cart/', include('cart.api.router')),
    path('payment/', include('payment.urls')),
    path('order/', include('order.api.routers')),
    path('delivery/', include('delivery.api.routers')),
]

if settings.DEBUG == True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
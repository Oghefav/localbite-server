from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title='localbite API',
        default_version= 1,
        description = 'Localbite API Documentation',
        contact=openapi.Contact(email='favouroghenevwoke@gmail.com'),
        terms_of_service='https://www.google.com/policies/terms/',
        license=openapi.License(name ='Localbite license')
    ),
    authentication_classes=[],
    permission_classes=[AllowAny],
    public=False
)
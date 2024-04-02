from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers


schema_view = get_schema_view(
   openapi.Info(
      title="Discord API",
      default_version='v1',   
      description="API de comunicação Discord",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="gugusoliveira72@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("core.urls")),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
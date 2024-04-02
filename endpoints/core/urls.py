
from django.urls import path, include
from rest_framework import routers
from .views import CommunityViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

rota = routers.DefaultRouter()
rota.register("community", CommunityViewSet, basename="Community")


urlpatterns = [
    path('', include(rota.urls), name='api'),
    path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh_pair"),

]
    
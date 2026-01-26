from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from .views import UserRegistration, UserLogin

urlpatterns = [
    #api routes
    path('api/auth/user-register/', UserRegistration.as_view(), name='use-register'),
    path('api/auth/user-login/', UserLogin.as_view(), name='user-login'),


]
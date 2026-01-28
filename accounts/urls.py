from django.urls import path
from .views import UserRegistration, UserLogin, AccessTokenRefresh, UserProfile

urlpatterns = [
    #api routes
    path('api/auth/user-register/', UserRegistration.as_view(), name='use-register'),
    path('api/auth/user-login/', UserLogin.as_view(), name='user-login'),
    path('api/auth/token/refresh/', AccessTokenRefresh.as_view(), name='token-refresh'),
    path('api/auth/user-profile/', UserProfile.as_view(), name='user-profile'),
]
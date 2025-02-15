from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Default view for the root URL
def home(request):
    return HttpResponse("Welcome to the Currency API! Go to /api/rates/ to check exchange rates.")


urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('auth/register/', include('accounts.urls')),  # We'll add accounts/urls.py next
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('currency.urls')),  # Currency API endpoints
]

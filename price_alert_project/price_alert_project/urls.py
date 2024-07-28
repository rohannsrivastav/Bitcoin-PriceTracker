from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from alerts.coingecko_api import coingecko_api
import threading

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/alerts/', include('alerts.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

def start_coingecko_api():
    api_thread = threading.Thread(target=coingecko_api.run)
    api_thread.daemon = True
    api_thread.start()

start_coingecko_api()
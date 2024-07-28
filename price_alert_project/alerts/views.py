from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Alert
from .serializers import AlertSerializer, AlertListSerializer
import requests

class CreateAlertView(generics.CreateAPIView):
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cryptocurrency = serializer.validated_data['cryptocurrency']
        initial_price = self.get_current_price(cryptocurrency)
        serializer.save(user=self.request.user, initial_price=initial_price)

    def get_current_price(self, cryptocurrency):
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "inr",
            "order": "market_cap_desc",
            "per_page": 100,
            "page": 1,
            "sparkline": "false"
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            coin_data = response.json()
            for coin in coin_data:
                if coin['symbol'].upper() == cryptocurrency.upper():
                    return float(coin['current_price'])
        return None

class CreateAlertView(generics.CreateAPIView):
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DeleteAlertView(generics.DestroyAPIView):
    queryset = Alert.objects.all()
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({"detail": "You do not have permission to delete this alert."}, status=status.HTTP_403_FORBIDDEN)
        instance.status = 'deleted'
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AlertListView(generics.ListAPIView):
    serializer_class = AlertListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['created_at', 'updated_at']

    def get_queryset(self):
        return Alert.objects.filter(user=self.request.user)
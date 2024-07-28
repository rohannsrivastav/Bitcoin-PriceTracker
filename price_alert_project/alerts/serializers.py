from rest_framework import serializers
from .models import Alert

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id', 'cryptocurrency', 'target_price', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']

class AlertListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id', 'cryptocurrency', 'target_price', 'status', 'created_at', 'updated_at']
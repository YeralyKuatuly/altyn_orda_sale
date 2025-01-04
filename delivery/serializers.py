from rest_framework import serializers
from .models import Courier, Delivery, DeliveryStatusHistory
from accounts.serializers import UserSerializer


class CourierSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Courier
        fields = [
            'id', 'user', 'user_id', 'courier_type', 'status',
            'phone', 'current_location', 'created_at'
        ]
        read_only_fields = ['created_at']


class DeliveryStatusHistorySerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = DeliveryStatusHistory
        fields = [
            'id', 'delivery', 'status', 'location',
            'notes', 'created_at', 'created_by'
        ]
        read_only_fields = ['created_at', 'created_by']


class DeliverySerializer(serializers.ModelSerializer):
    courier = CourierSerializer(read_only=True)
    courier_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    status_history = DeliveryStatusHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Delivery
        fields = [
            'id', 'order', 'courier', 'courier_id', 'status',
            'pickup_location', 'delivery_location',
            'estimated_delivery_time', 'actual_delivery_time',
            'created_at', 'updated_at', 'status_history'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        courier_id = validated_data.pop('courier_id', None)
        if courier_id:
            validated_data['courier'] = Courier.objects.get(id=courier_id)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        courier_id = validated_data.pop('courier_id', None)
        if courier_id:
            validated_data['courier'] = Courier.objects.get(id=courier_id)
        return super().update(instance, validated_data)

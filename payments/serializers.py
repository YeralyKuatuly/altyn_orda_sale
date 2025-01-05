from rest_framework import serializers
from .models import PaymentProvider, Payment, PaymentLog, Receipt
from orders.serializers import OrderSerializer


class PaymentProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentProvider
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['created_at']


class PaymentLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentLog
        fields = [
            'id', 'payment', 'provider', 'request_body',
            'response_body', 'status_code', 'created_at'
        ]
        read_only_fields = ['created_at']


class PaymentSerializer(serializers.ModelSerializer):
    logs = PaymentLogSerializer(many=True, read_only=True)
    order = OrderSerializer(read_only=True)
    order_id = serializers.IntegerField(write_only=True)
    provider = PaymentProviderSerializer(read_only=True)
    provider_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Payment
        fields = [
            'id', 'order', 'order_id', 'provider', 'provider_id',
            'amount', 'payment_method', 'status', 'transaction_id',
            'provider_signature', 'created_at', 'updated_at', 'logs'
        ]
        read_only_fields = ['created_at', 'updated_at', 'transaction_id', 'provider_signature']


class ReceiptSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)
    payment_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Receipt
        fields = [
            'id', 'order', 'payment', 'payment_id', 'procurement',
            'total_amount', 'created_at', 'receipt_number'
        ]
        read_only_fields = ['created_at', 'receipt_number']

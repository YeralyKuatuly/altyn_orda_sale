from rest_framework import serializers
from .models import Purchaser, Procurement
from accounts.serializers import UserSerializer
from inventory.serializers import ProductSerializer
from delivery.serializers import CourierSerializer
from inventory.models import Product, Warehouse
from delivery.models import Courier


class PurchaserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Purchaser
        fields = ['id', 'user', 'user_id', 'created_at']
        read_only_fields = ['created_at']


class ProcurementSerializer(serializers.ModelSerializer):
    purchaser_id = serializers.PrimaryKeyRelatedField(
        queryset=Purchaser.objects.all(),
        source='purchaser'
    )
    warehouse_courier_id = serializers.PrimaryKeyRelatedField(
        queryset=Courier.objects.all(),
        source='warehouse_courier'
    )
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product'
    )
    warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(),
        source='warehouse'
    )

    class Meta:
        model = Procurement
        fields = [
            'id', 'purchaser_id', 'warehouse_courier_id',
            'product_id', 'quantity', 'price', 'warehouse_id',
            'created_at'
        ]
        read_only_fields = ['created_at']

    def validate(self, data):
        if data.get('quantity', 0) <= 0:
            raise serializers.ValidationError({"quantity": "Quantity must be positive"})
        if float(data.get('price', 0)) <= 0:
            raise serializers.ValidationError({"price": "Price must be positive"})
        return data

from rest_framework import serializers
from decimal import Decimal
from .models import Order, OrderItem, OrderChangeHistory

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price']
        
    def validate(self, data):
        if data['quantity'] <= 0:
            raise serializers.ValidationError({"quantity": "Quantity must be positive"})
        if data['price'] <= 0:
            raise serializers.ValidationError({"price": "Price must be positive"})
        return data

class OrderChangeHistorySerializer(serializers.ModelSerializer):
    changed_by_username = serializers.ReadOnlyField(source='changed_by.username')
    
    class Meta:
        model = OrderChangeHistory
        fields = [
            'id', 
            'order', 
            'changed_by', 
            'changed_by_username',
            'field_name', 
            'old_value', 
            'new_value', 
            'changed_at'
        ]
        read_only_fields = ['changed_at', 'changed_by']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_price = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    change_history = OrderChangeHistorySerializer(
        many=True, 
        read_only=True
    )

    class Meta:
        model = Order
        fields = [
            'id',
            'order_number',
            'user',
            'status',
            'total_price',
            'delivery_address',
            'items',
            'change_history',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'order_number',
            'status',
            'total_price',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        total_price = Decimal('0')

        for item_data in items_data:
            OrderItem.objects.create(
                order=order,
                **item_data
            )
            total_price += Decimal(str(item_data['quantity'])) * Decimal(str(item_data['price']))

        order.total_price = total_price
        order.save()
        return order

    def update(self, instance, validated_data):
        if instance.status == 'completed':
            raise serializers.ValidationError("Cannot modify completed orders")

        items_data = validated_data.pop('items', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if items_data is not None:
            instance.items.all().delete()
            total_price = Decimal('0')

            for item_data in items_data:
                OrderItem.objects.create(
                    order=instance,
                    **item_data
                )
                total_price += Decimal(str(item_data['quantity'])) * Decimal(str(item_data['price']))

            instance.total_price = total_price

        instance.save()
        return instance
from rest_framework import serializers
from .models import Category, Product, Stock, Warehouse, WarehouseLog


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent_category', 'subcategories', 'created_at']

    def get_subcategories(self, obj):
        subcategories = obj.subcategories.all()
        return CategorySerializer(subcategories, many=True).data


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'category', 'created_at', 'updated_at']


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'address', 'product', 'quantity', 'updated_at']


class WarehouseLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseLog
        fields = ['id', 'product', 'quantity', 'operation_type', 'created_at']

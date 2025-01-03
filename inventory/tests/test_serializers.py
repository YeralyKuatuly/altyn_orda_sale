from django.test import TestCase
from inventory.models import Category, Product, Stock
from inventory.serializers import CategorySerializer, ProductSerializer, StockSerializer


class CategorySerializerTest(TestCase):
    def test_serialize_category(self):
        category = Category.objects.create(name="Electronics")
        serializer = CategorySerializer(category)
        self.assertEqual(serializer.data['name'], "Electronics")


class ProductSerializerTest(TestCase):
    def test_serialize_product(self):
        category = Category.objects.create(name="Electronics")
        product = Product.objects.create(name="Smartphone", price=999.99, stock=10, category=category)
        serializer = ProductSerializer(product)
        self.assertEqual(serializer.data['name'], "Smartphone")
        self.assertEqual(serializer.data['price'], "999.99")


class StockSerializerTest(TestCase):
    def test_serialize_stock(self):
        category = Category.objects.create(name="Electronics")
        product = Product.objects.create(name="Smartphone", price=999.99, stock=10, category=category)
        stock = Stock.objects.create(product=product, quantity=50, location="Warehouse A")
        serializer = StockSerializer(stock)
        self.assertEqual(serializer.data['quantity'], 50)
        self.assertEqual(serializer.data['location'], "Warehouse A")

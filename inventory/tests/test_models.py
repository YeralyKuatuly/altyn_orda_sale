from django.test import TestCase
from inventory.models import Category, Product, Stock


class CategoryModelTest(TestCase):
    def test_create_category(self):
        category = Category.objects.create(name="Electronics")
        self.assertEqual(category.name, "Electronics")
        self.assertIsNotNone(category.created_at)


class ProductModelTest(TestCase):
    def test_create_product(self):
        category = Category.objects.create(name="Electronics")
        product = Product.objects.create(
            name="Smartphone", description="A new smartphone", price=999.99, stock=10, category=category
        )
        self.assertEqual(product.name, "Smartphone")
        self.assertEqual(product.price, 999.99)
        self.assertEqual(product.stock, 10)
        self.assertEqual(product.category, category)


class StockModelTest(TestCase):
    def test_create_stock(self):
        category = Category.objects.create(name="Electronics")
        product = Product.objects.create(name="Smartphone", price=999.99, stock=10, category=category)
        stock = Stock.objects.create(product=product, quantity=50, location="Warehouse A")
        self.assertEqual(stock.product, product)
        self.assertEqual(stock.quantity, 50)
        self.assertEqual(stock.location, "Warehouse A")

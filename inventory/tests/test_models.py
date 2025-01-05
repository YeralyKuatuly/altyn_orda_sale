# inventory/tests/test_models.py
from django.test import TestCase
from decimal import Decimal
from inventory.models import Category, Product, Stock, Warehouse, WarehouseLog


class CategoryModelTests(TestCase):
    def setUp(self):
        self.parent_category = Category.objects.create(name="Food")
        self.child_category = Category.objects.create(
            name="Fruits",
            parent_category=self.parent_category
        )

    def test_category_str_representation(self):
        """Test the string representation of Category model"""
        self.assertEqual(str(self.parent_category), "Food")
        self.assertEqual(str(self.child_category), "Food -> Fruits")

    def test_category_creation(self):
        """Test category creation and relationships"""
        self.assertEqual(self.child_category.parent_category, self.parent_category)
        self.assertTrue(self.parent_category.subcategories.filter(id=self.child_category.id).exists())


class ProductModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Laptop",
            description="A powerful laptop",
            price=Decimal("999.99"),
            stock=10,
            category=self.category
        )

    def test_product_str_representation(self):
        """Test the string representation of Product model"""
        self.assertEqual(str(self.product), "Laptop")

    def test_product_price_precision(self):
        """Test that price field maintains decimal precision"""
        self.assertEqual(self.product.price, Decimal("999.99"))


class StockModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Laptop",
            price=Decimal("999.99"),
            category=self.category
        )
        self.stock = Stock.objects.create(
            product=self.product,
            quantity=50,
            location="Warehouse A"
        )

    def test_stock_str_representation(self):
        """Test the string representation of Stock model"""
        self.assertEqual(str(self.stock), "Laptop - 50")


class WarehouseModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Laptop",
            price=Decimal("999.99"),
            category=self.category
        )
        self.warehouse = Warehouse.objects.create(
            name="Main Warehouse",
            address="123 Storage St",
            product=self.product,
            quantity=50
        )

    def test_warehouse_str_representation(self):
        """Test the string representation of Warehouse model"""
        self.assertEqual(str(self.warehouse), "Main Warehouse - Laptop")

    def test_warehouse_quantity(self):
        """Test warehouse quantity management"""
        self.assertEqual(self.warehouse.quantity, 50)


class WarehouseLogModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Laptop",
            price=Decimal("999.99"),
            category=self.category
        )
        self.log = WarehouseLog.objects.create(
            product=self.product,
            quantity=10,
            operation_type='arrival'
        )

    def test_log_str_representation(self):
        """Test the string representation of WarehouseLog model"""
        self.assertEqual(str(self.log), "arrival - Laptop (10)")

    def test_log_operation_types(self):
        """Test warehouse log operation types"""
        # Test arrival operation
        arrival_log = WarehouseLog.objects.create(
            product=self.product,
            quantity=15,
            operation_type='arrival'
        )
        self.assertEqual(arrival_log.operation_type, 'arrival')

        # Test expense operation
        expense_log = WarehouseLog.objects.create(
            product=self.product,
            quantity=5,
            operation_type='expense'
        )
        self.assertEqual(expense_log.operation_type, 'expense')

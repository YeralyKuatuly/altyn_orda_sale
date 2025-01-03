from rest_framework import status
from inventory.models import Category, Product, Stock
from inventory.tests.test_base import AuthenticatedAPITestCase


class CategoryAPITest(AuthenticatedAPITestCase):
    def test_create_category(self):
        response = self.client.post('/api/inventory/categories/', {"name": "Electronics"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Electronics")

    def test_list_categories(self):
        Category.objects.create(name="Electronics")
        response = self.client.get('/api/inventory/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ProductAPITest(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.category = Category.objects.create(name="Electronics")

    def test_create_product(self):
        data = {
            "name": "Smartphone",
            "price": 999.99,
            "stock": 10,
            "category": self.category.id
        }
        response = self.client.post('/api/inventory/products/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Smartphone")

    def test_list_products(self):
        Product.objects.create(name="Smartphone", price=999.99, stock=10, category=self.category)
        response = self.client.get('/api/inventory/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class StockAPITest(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(name="Smartphone", price=999.99, stock=10, category=self.category)

    def test_create_stock(self):
        data = {
            "product": self.product.id,
            "quantity": 50,
            "location": "Warehouse A"
        }
        response = self.client.post('/api/inventory/stocks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['quantity'], 50)

    def test_list_stocks(self):
        Stock.objects.create(product=self.product, quantity=50, location="Warehouse A")
        response = self.client.get('/api/inventory/stocks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

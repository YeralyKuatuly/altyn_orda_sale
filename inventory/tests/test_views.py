from django.urls import reverse
from rest_framework import status
from decimal import Decimal
from inventory.models import Category, Product, Stock
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()


class AuthenticatedAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass")
        # Generate a JWT token
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        # Add the token to the default headers
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")


class CategoryViewTests(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()  # Call parent setUp to handle authentication
        self.category = Category.objects.create(name="Electronics")
        self.child_category = Category.objects.create(
            name="Phones",
            parent_category=self.category
        )

    def test_category_list_view(self):
        """Test category list endpoint"""
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Parent and child category

    def test_create_category(self):
        """Test creating a new category"""
        url = reverse('category-list')
        data = {'name': 'Books'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 3)
        self.assertEqual(Category.objects.get(name='Books').name, 'Books')

    def test_unauthorized_access(self):
        """Test that unauthorized access is prevented"""
        self.client.credentials()  # Remove authentication
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProductViewTests(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()  # Call parent setUp to handle authentication
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Laptop",
            price=Decimal("999.99"),
            category=self.category,
            stock=10
        )

    def test_product_list_view(self):
        """Test product list endpoint"""
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_product_filter_by_category(self):
        """Test product filtering by category"""
        url = f"{reverse('product-list')}?category_id={self.category.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Laptop")

    def test_delete_product(self):
        """Test deleting a product"""
        url = reverse('product-detail', kwargs={'pk': self.product.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)


class StockViewTests(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()  # Call parent setUp to handle authentication
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

    def test_stock_list(self):
        """Test stock list endpoint"""
        url = reverse('stock-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_stock_update(self):
        """Test stock update endpoint"""
        url = reverse('stock-detail', kwargs={'pk': self.stock.id})
        updated_data = {
            'product': self.product.id,
            'quantity': 75,
            'location': "Warehouse B"
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 75)
        self.assertEqual(response.data['location'], "Warehouse B")

    def test_create_stock(self):
        """Test creating a new stock entry"""
        url = reverse('stock-list')
        data = {
            'product': self.product.id,
            'quantity': 100,
            'location': "Warehouse C"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Stock.objects.count(), 2)
        self.assertEqual(Stock.objects.latest('id').location, "Warehouse C")

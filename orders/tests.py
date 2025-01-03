from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from decimal import Decimal
from django.contrib.auth import get_user_model
from inventory.models import Product
from .models import Order, OrderItem, OrderChangeHistory
from .serializers import OrderSerializer, OrderItemSerializer, OrderChangeHistorySerializer

User = get_user_model()

class OrderModelTests(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        # Create product
        self.product = Product.objects.create(
            name='Test Product',
            price=Decimal('10.00')
        )

    def test_order_creation(self):
        """Test creating an order"""
        order = Order.objects.create(
            user=self.user,
            delivery_address='Test Address 123'
        )
        self.assertIsNotNone(order.order_number)
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.total_price, Decimal('0.00'))
        self.assertEqual(str(order), f"Order #{order.order_number} by {self.user.username}")

    def test_order_item_creation(self):
        """Test creating an order item"""
        order = Order.objects.create(
            user=self.user,
            delivery_address='Test Address 123'
        )
        order_item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
            price=self.product.price
        )
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.price, Decimal('10.00'))
        self.assertEqual(str(order_item), f"{self.product.name} x2")

    def test_order_change_history(self):
        """Test order change history creation"""
        order = Order.objects.create(
            user=self.user,
            delivery_address='Test Address 123'
        )
        history = OrderChangeHistory.objects.create(
            order=order,
            changed_by=self.user,
            field_name='status',
            old_value='pending',
            new_value='completed'
        )
        self.assertEqual(
            str(history),
            f"Change in Order #{order.order_number} by {self.user.username}"
        )

class OrderSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.product = Product.objects.create(
            name='Test Product',
            price=Decimal('10.00')
        )

    def test_valid_order_serializer(self):
        """Test order serializer with valid data"""
        data = {
            'delivery_address': 'Test Address 123',
            'items': [
                {
                    'product': self.product.id,
                    'quantity': 2,
                    'price': '10.00'
                }
            ]
        }
        context = {'request': type('Obj', (), {'user': self.user})}
        serializer = OrderSerializer(data=data, context=context)
        self.assertTrue(serializer.is_valid())

    def test_invalid_order_serializer(self):
        """Test order serializer with invalid data"""
        data = {
            'delivery_address': '',  # Empty address
            'items': [
                {
                    'product': self.product.id,
                    'quantity': -1,  # Invalid quantity
                    'price': '-10.00'  # Invalid price
                }
            ]
        }
        context = {'request': type('Obj', (), {'user': self.user})}
        serializer = OrderSerializer(data=data, context=context)
        self.assertFalse(serializer.is_valid())
        self.assertIn('delivery_address', serializer.errors)

class OrderAPITests(APITestCase):
    def setUp(self):
        # Create users
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.staff_user = User.objects.create_user(
            username='staffuser',
            password='staffpass123',
            is_staff=True
        )
        
        # Create product
        self.product = Product.objects.create(
            name='Test Product',
            price=Decimal('10.00')
        )
        
        # Prepare order data
        self.order_data = {
            'delivery_address': 'Test Address 123',
            'items': [
                {
                    'product': self.product.id,
                    'quantity': 2,
                    'price': '10.00'
                }
            ]
        }
        self.client.force_authenticate(user=self.user)

    def test_create_order(self):
        """Test creating an order through API"""
        url = reverse('order-list')
        response = self.client.post(url, self.order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)

    def test_list_orders(self):
        """Test listing orders"""
        Order.objects.create(user=self.user, delivery_address='Test Address')
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_change_order_status(self):
        """Test changing order status"""
        order = Order.objects.create(
            user=self.user,
            delivery_address='Test Address'
        )
        url = reverse('order-change-status', kwargs={'pk': order.pk})

        # Test with regular user (should fail)
        response = self.client.patch(url, {'status': 'completed'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Test with staff user (should succeed)
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.patch(url, {'status': 'completed'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify status change and history creation
        order.refresh_from_db()
        self.assertEqual(order.status, 'completed')
        self.assertTrue(OrderChangeHistory.objects.exists())

    def test_unauthorized_access(self):
        """Test unauthorized access to orders"""
        self.client.logout()
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class OrderItemAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.product = Product.objects.create(
            name='Test Product',
            price=Decimal('10.00')
        )
        self.order = Order.objects.create(
            user=self.user,
            delivery_address='Test Address'
        )
        self.client.force_authenticate(user=self.user)

    def test_list_order_items(self):
        """Test listing order items"""
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=Decimal('10.00')
        )
        url = reverse('orderitem-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_item_detail(self):
        """Test retrieving order item detail"""
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=Decimal('10.00')
        )
        url = reverse('orderitem-detail', kwargs={'pk': item.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 2)

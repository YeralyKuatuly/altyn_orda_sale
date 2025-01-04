from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from decimal import Decimal
from django.contrib.auth import get_user_model
from inventory.models import Category, Product
from .models import Order, OrderItem, OrderChangeHistory
from .serializers import OrderSerializer

User = get_user_model()


class OrderModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            price=Decimal('10.00'),
            stock=50,
            category=self.category
        )

    def test_order_creation(self):
        order = Order.objects.create(
            user=self.user,
            delivery_address='Test Address'
        )
        self.assertIsNotNone(order.order_number)
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.total_price, Decimal('0.00'))

    def test_order_item_creation(self):
        order = Order.objects.create(
            user=self.user,
            delivery_address='Test Address'
        )
        order_item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
            price=self.product.price
        )
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.price, Decimal('10.00'))


class OrderAPITests(APITestCase):
    def setUp(self):
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
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            price=Decimal('10.00'),
            stock=50,
            category=self.category
        )
        self.order_data = {
            'delivery_address': 'Test Address 123',
            'items': [
                {
                    'product': self.product.id,
                    'quantity': 2,
                    'price': str(self.product.price)
                }
            ]
        }
        self.client.force_authenticate(user=self.user)

    def test_create_order(self):
        url = reverse('order-list')
        response = self.client.post(url, self.order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)

    def test_change_order_status(self):
        order = Order.objects.create(
            user=self.user,
            delivery_address='Test Address'
        )
        url = reverse('order-change-status', kwargs={'pk': order.pk})

        response = self.client.patch(url, {'status': 'completed'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.staff_user)
        response = self.client.patch(url, {'status': 'completed'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order.refresh_from_db()
        self.assertEqual(order.status, 'completed')
        self.assertEqual(
            OrderChangeHistory.objects.filter(order=order).count(),
            1
        )

    def test_list_orders(self):
        Order.objects.create(
            user=self.user,
            delivery_address='Test Address'
        )
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_staff_access_all_orders(self):
        Order.objects.create(
            user=self.user,
            delivery_address='Test Address'
        )
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class OrderItemAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            price=Decimal('10.00'),
            stock=50,
            category=self.category
        )
        self.order = Order.objects.create(
            user=self.user,
            delivery_address='Test Address'
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=Decimal('10.00')
        )
        self.client.force_authenticate(user=self.user)

    def test_list_order_items(self):
        url = reverse('orderitem-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

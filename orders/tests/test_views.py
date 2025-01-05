from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from decimal import Decimal
from .factories import (
    UserFactory, CategoryFactory,
    ProductFactory, OrderFactory,
    OrderItemFactory
)
from orders.models import Order, OrderItem, OrderChangeHistory


class OrderAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.staff_user = UserFactory(
            username='staffuser',
            is_staff=True
        )
        self.category = CategoryFactory()
        self.product = ProductFactory(category=self.category)
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
        order = OrderFactory(user=self.user)
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
        OrderFactory(user=self.user)
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_staff_access_all_orders(self):
        OrderFactory(user=self.user)
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class OrderItemAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.category = CategoryFactory()
        self.product = ProductFactory(category=self.category)
        self.order = OrderFactory(user=self.user)
        self.order_item = OrderItemFactory(
            order=self.order,
            product=self.product
        )
        self.client.force_authenticate(user=self.user)

    def test_list_order_items(self):
        url = reverse('orderitem-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

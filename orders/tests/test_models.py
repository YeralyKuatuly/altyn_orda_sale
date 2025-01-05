from django.test import TestCase
from decimal import Decimal
from .test_factories import (
    UserFactory, CategoryFactory,
    ProductFactory, OrderFactory,
    OrderItemFactory
)


class OrderModelTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.category = CategoryFactory()
        self.product = ProductFactory(category=self.category)

    def test_order_creation(self):
        order = OrderFactory(user=self.user)
        self.assertIsNotNone(order.order_number)
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.total_price, Decimal('0.00'))

    def test_order_item_creation(self):
        order = OrderFactory(user=self.user)
        order_item = OrderItemFactory(
            order=order,
            product=self.product
        )
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.price, Decimal('10.00'))

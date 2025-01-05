from django.test import TestCase
from django.core.exceptions import ValidationError
from .test_factories import (
    UserFactory, CourierFactory,
    DeliveryFactory, DeliveryStatusHistoryFactory,
    DeliveryLogFactory, CourierDeliveryHistoryFactory
)
from orders.tests.test_factories import OrderFactory


class CourierModelTest(TestCase):
    def setUp(self):
        self.courier = CourierFactory()

    def test_courier_creation(self):
        self.assertTrue(isinstance(self.courier.user.username, str))
        self.assertEqual(self.courier.status, 'available')

    def test_courier_str_representation(self):
        expected_str = f"{self.courier.user.username} - Client Courier"
        self.assertEqual(str(self.courier), expected_str)

    def test_courier_type_choices(self):
        courier = CourierFactory(courier_type='invalid')
        with self.assertRaises(ValidationError):
            courier.full_clean()


class DeliveryModelTest(TestCase):
    def setUp(self):
        self.delivery = DeliveryFactory()

    def test_delivery_creation(self):
        self.assertEqual(self.delivery.status, 'pending')
        self.assertIsNotNone(self.delivery.created_at)

    def test_delivery_str_representation(self):
        expected_str = f"Delivery for Order #{self.delivery.order.order_number}"
        self.assertEqual(str(self.delivery), expected_str)


class DeliveryStatusHistoryModelTest(TestCase):
    def setUp(self):
        self.history = DeliveryStatusHistoryFactory()

    def test_status_history_creation(self):
        self.assertEqual(self.history.status, 'pending')
        self.assertIsNotNone(self.history.created_at)


class DeliveryLogModelTest(TestCase):
    def setUp(self):
        self.delivery_log = DeliveryLogFactory()

    def test_delivery_log_creation(self):
        self.assertIsNotNone(self.delivery_log.message)
        self.assertIsNotNone(self.delivery_log.created_at)

    def test_delivery_log_str_representation(self):
        expected_str = f"Log for delivery #{self.delivery_log.delivery.id}"
        self.assertEqual(str(self.delivery_log), expected_str)


class CourierDeliveryHistoryModelTest(TestCase):
    def setUp(self):
        self.history = CourierDeliveryHistoryFactory()

    def test_courier_delivery_history_creation(self):
        self.assertIsNotNone(self.history.delivered_at)

    def test_courier_delivery_history_str_representation(self):
        expected_str = (f"Delivery by {self.history.courier.user.username} "
                       f"for order #{self.history.order.order_number}")
        self.assertEqual(str(self.history), expected_str)

    def test_courier_delivered_orders_count(self):
        courier = CourierFactory(delivered_orders_count=0)
        order = OrderFactory()
        CourierDeliveryHistoryFactory(courier=courier, order=order)
        courier.delivered_orders_count += 1
        courier.save()
        self.assertEqual(courier.delivered_orders_count, 1)

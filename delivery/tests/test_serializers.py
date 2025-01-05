from django.test import TestCase
from delivery.serializers import (
    CourierSerializer,
    DeliverySerializer,
    DeliveryStatusHistorySerializer,
    DeliveryLogSerializer,
    CourierDeliveryHistorySerializer
)
from .factories import (
    UserFactory, CourierFactory,
    DeliveryFactory, DeliveryStatusHistoryFactory,
    DeliveryLogFactory, CourierDeliveryHistoryFactory
)


class CourierSerializerTest(TestCase):
    def setUp(self):
        self.courier = CourierFactory()
        self.serializer = CourierSerializer(instance=self.courier)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        expected_fields = {
            'id', 'user', 'courier_type', 'status',
            'phone', 'current_location', 'created_at'
        }
        self.assertEqual(set(data.keys()), expected_fields)

    def test_valid_serializer_data(self):
        user = UserFactory()
        data = {
            'user_id': user.id,
            'courier_type': 'client',
            'status': 'available',
            'phone': '+77071234567',
            'current_location': 'Test Location'
        }
        serializer = CourierSerializer(data=data)
        self.assertTrue(serializer.is_valid())


class DeliverySerializerTest(TestCase):
    def setUp(self):
        self.delivery = DeliveryFactory()
        self.serializer = DeliverySerializer(instance=self.delivery)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        expected_fields = {
            'id', 'order', 'courier', 'status', 'pickup_location',
            'delivery_location', 'estimated_delivery_time',
            'actual_delivery_time', 'created_at', 'updated_at',
            'status_history'
        }
        self.assertEqual(set(data.keys()), expected_fields)


class DeliveryLogSerializerTest(TestCase):
    def setUp(self):
        self.delivery_log = DeliveryLogFactory()
        self.serializer = DeliveryLogSerializer(instance=self.delivery_log)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        expected_fields = {'id', 'delivery', 'message', 'created_at'}
        self.assertEqual(set(data.keys()), expected_fields)


class CourierDeliveryHistorySerializerTest(TestCase):
    def setUp(self):
        self.history = CourierDeliveryHistoryFactory()
        self.serializer = CourierDeliveryHistorySerializer(instance=self.history)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        expected_fields = {'id', 'courier', 'order', 'delivered_at'}
        self.assertEqual(set(data.keys()), expected_fields)

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .factories import (
    UserFactory, CourierFactory,
    DeliveryFactory, DeliveryStatusHistoryFactory,
    DeliveryLogFactory, CourierDeliveryHistoryFactory,
    OrderFactory
)


class CourierViewSetTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.courier = CourierFactory()

    def test_list_couriers(self):
        url = reverse('courier-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_courier(self):
        url = reverse('courier-list')
        user = UserFactory()
        data = {
            'user_id': user.id,
            'courier_type': 'client',
            'status': 'available',
            'phone': '+77071234567',
            'current_location': 'Test Location'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_courier_location(self):
        url = reverse('courier-update-location', kwargs={'pk': self.courier.pk})
        data = {'location': 'New Location'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeliveryViewSetTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.delivery = DeliveryFactory()

    def test_list_deliveries(self):
        url = reverse('delivery-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_assign_courier(self):
        url = reverse('delivery-assign-courier', kwargs={'pk': self.delivery.pk})
        courier = CourierFactory()
        data = {'courier_id': courier.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_delivery_status(self):
        url = reverse('delivery-update-status', kwargs={'pk': self.delivery.pk})
        data = {
            'status': 'in_transit',
            'notes': 'Test status update',
            'location': 'Test Location'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeliveryLogViewSetTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.delivery_log = DeliveryLogFactory()

    def test_list_delivery_logs(self):
        url = reverse('delivery-log-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_delivery_log(self):
        url = reverse('delivery-log-list')
        delivery = DeliveryFactory()
        data = {
            'delivery': delivery.id,
            'message': 'Test log message'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CourierDeliveryHistoryViewSetTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.history = CourierDeliveryHistoryFactory()

    def test_list_courier_history(self):
        url = reverse('courier-history-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_courier_history(self):
        url = reverse('courier-history-list')
        courier = CourierFactory()
        order = OrderFactory()
        data = {
            'courier': courier.id,
            'order': order.id,
            'delivered_at': '2025-01-05T12:00:00Z'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

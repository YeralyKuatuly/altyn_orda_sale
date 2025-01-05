from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .test_factories import PurchaserFactory, ProcurementFactory, UserFactory


class PurchaserViewSetTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.purchaser = PurchaserFactory()

    def test_list_purchasers(self):
        url = reverse('purchaser-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_purchaser(self):
        url = reverse('purchaser-list')
        user = UserFactory()
        data = {
            'user_id': user.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_procurement_history(self):
        url = reverse('purchaser-procurement-history', kwargs={'pk': self.purchaser.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProcurementViewSetTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.procurement = ProcurementFactory()

    def test_list_procurements(self):
        url = reverse('procurement-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_procurement(self):
        url = reverse('procurement-list')
        data = {
            'purchaser_id': self.procurement.purchaser.id,
            'warehouse_courier_id': self.procurement.warehouse_courier.id,
            'product_id': self.procurement.product.id,
            'warehouse_id': self.procurement.warehouse.id,
            'quantity': 10,
            'price': "100.00"
        }

        # Force format to be JSON and print response data for debugging
        response = self.client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .factories import PaymentProviderFactory, PaymentFactory, ReceiptFactory
from accounts.tests.factories import UserFactory


class PaymentViewSetTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.payment = PaymentFactory()

    def test_list_payments(self):
        url = reverse('payment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_process_payment(self):
        url = reverse('payment-process-payment', kwargs={'pk': self.payment.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.status, 'completed')

    def test_refund_payment(self):
        self.payment.status = 'completed'
        self.payment.save()
        url = reverse('payment-refund', kwargs={'pk': self.payment.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.status, 'refunded')


class ReceiptViewSetTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.receipt = ReceiptFactory()

    def test_list_receipts(self):
        url = reverse('receipt-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_download_receipt(self):
        url = reverse('receipt-download', kwargs={'pk': self.receipt.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

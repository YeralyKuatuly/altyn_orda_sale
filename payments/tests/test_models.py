from django.test import TestCase
from .test_factories import PaymentProviderFactory, PaymentFactory, PaymentLogFactory, ReceiptFactory


class PaymentProviderTest(TestCase):
    def setUp(self):
        self.provider = PaymentProviderFactory()

    def test_provider_creation(self):
        self.assertIsNotNone(self.provider.name)
        self.assertIsNotNone(self.provider.created_at)


class PaymentTest(TestCase):
    def setUp(self):
        self.payment = PaymentFactory()

    def test_payment_creation(self):
        self.assertEqual(self.payment.status, 'pending')
        self.assertIsNotNone(self.payment.created_at)
        self.assertTrue(self.payment.amount > 0)

    def test_payment_str_representation(self):
        expected_str = f"Payment {self.payment.id} for Order {self.payment.order.order_number}"
        self.assertEqual(str(self.payment), expected_str)


class ReceiptTest(TestCase):
    def setUp(self):
        self.receipt = ReceiptFactory()

    def test_receipt_creation(self):
        self.assertIsNotNone(self.receipt.receipt_number)
        self.assertTrue(self.receipt.receipt_number.startswith('RCP-'))

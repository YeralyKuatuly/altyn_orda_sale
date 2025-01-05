from django.test import TestCase
from django.core.exceptions import ValidationError
from .test_factories import PurchaserFactory, ProcurementFactory


class PurchaserModelTest(TestCase):
    def setUp(self):
        self.purchaser = PurchaserFactory()

    def test_purchaser_creation(self):
        self.assertTrue(isinstance(self.purchaser.user.username, str))
        self.assertIsNotNone(self.purchaser.created_at)

    def test_purchaser_str_representation(self):
        expected_str = f"Purchaser: {self.purchaser.user.username}"
        self.assertEqual(str(self.purchaser), expected_str)


class ProcurementModelTest(TestCase):
    def setUp(self):
        self.procurement = ProcurementFactory()

    def test_procurement_creation(self):
        self.assertIsNotNone(self.procurement.purchaser)
        self.assertIsNotNone(self.procurement.created_at)
        self.assertTrue(self.procurement.quantity > 0)
        self.assertTrue(self.procurement.price > 0)

    def test_procurement_str_representation(self):
        expected_str = f"Procurement #{self.procurement.id} by {self.procurement.purchaser.user.username}"
        self.assertEqual(str(self.procurement), expected_str)

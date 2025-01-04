from django.test import TestCase
from inventory.models import Category, Product
from inventory.serializers import CategorySerializer


class CategorySerializerTests(TestCase):
    def setUp(self):
        self.parent_category = Category.objects.create(name="Food")
        self.child_category = Category.objects.create(
            name="Fruits",
            parent_category=self.parent_category
        )

    def test_serializer_contains_expected_fields(self):
        """Test that serializer contains all expected fields"""
        serializer = CategorySerializer(self.parent_category)
        expected_fields = {'id', 'name', 'parent_category', 'subcategories', 'created_at'}
        self.assertEqual(set(serializer.data.keys()), expected_fields)

    def test_nested_subcategories_serialization(self):
        """Test that subcategories are properly nested in serialization"""
        serializer = CategorySerializer(self.parent_category)
        self.assertEqual(len(serializer.data['subcategories']), 1)
        self.assertEqual(serializer.data['subcategories'][0]['name'], "Fruits")

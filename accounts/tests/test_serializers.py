from django.test import TestCase
from accounts.serializers import UserSerializer, ClientSerializer
from .test_factories import UserFactory, ClientFactory


class UserSerializerTests(TestCase):
    def setUp(self):
        self.user_data = {
            'telegram_id': '123456',
            'phone_number': '+1234567890',
            'email': 'test@example.com'
        }

    def test_serializer_with_valid_data(self):
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())

    def test_duplicate_telegram_id_validation(self):
        UserFactory(**self.user_data)
        serializer = UserSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('telegram_id', serializer.errors)


class ClientSerializerTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client_instance = ClientFactory(user=self.user)
        self.serializer = ClientSerializer(instance=self.client_instance)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        expected_fields = set(['id', 'user', 'created_at'])
        self.assertEqual(set(data.keys()), expected_fields)

    def test_user_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['user']['id'], self.user.id)
        self.assertEqual(data['user']['username'], self.user.username)

    def test_validate_unique_user(self):
        user = UserFactory()
        ClientFactory(user=user)  # Create existing client

        data = {
            'user_id': user.id
        }
        serializer = ClientSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('user_id', serializer.errors)

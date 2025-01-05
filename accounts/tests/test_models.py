from django.test import TestCase
from django.contrib.auth.hashers import check_password
from .test_factories import (
    UserFactory, RoleFactory, PermissionFactory,
    RolePermissionFactory, UserAddressFactory, ClientFactory
)
from accounts.models import Client


class UserModelTests(TestCase):
    def test_create_user_with_telegram_id(self):
        user = UserFactory(
            telegram_id='123456',
            phone_number='+1234567890',
            email='test@example.com'
        )
        self.assertTrue(user.is_telegram_user)
        self.assertEqual(user.telegram_id, '123456')
        # Changed to match the actual password creation logic
        self.assertTrue(check_password('telegram_user_default_password', user.password))
        self.assertEqual(user.username, user.telegram_id)

    def test_create_user_without_telegram_id(self):
        user = UserFactory(
            telegram_id=None,
            phone_number='+1234567890',
            email='test@example.com',
            username=None  # Force username to be None so it uses phone_number
        )
        self.assertFalse(user.is_telegram_user)
        self.assertEqual(user.username, user.phone_number)


class RolePermissionTests(TestCase):
    def test_create_role_permission(self):
        role_perm = RolePermissionFactory()
        expected_str = f'{role_perm.role.name} - {role_perm.permission.name}'
        self.assertEqual(str(role_perm), expected_str)


class UserAddressTests(TestCase):
    def test_user_address_creation(self):
        address = UserAddressFactory()
        expected_str = f'{address.user.username} - {address.address}'
        self.assertEqual(str(address), expected_str)
        self.assertIsNotNone(address.last_used_at)


class ClientModelTests(TestCase):
    def test_client_creation(self):
        client = ClientFactory()
        self.assertIsNotNone(client.user)
        self.assertIsNotNone(client.created_at)
        self.assertEqual(str(client), f"Client: {client.user.username}")

    def test_client_user_relationship(self):
        user = UserFactory()
        client = ClientFactory(user=user)
        self.assertEqual(client.user, user)
        self.assertEqual(user.client_profile, client)

    def test_delete_user_cascades_to_client(self):
        client = ClientFactory()
        user_id = client.user.id
        client.user.delete()
        self.assertEqual(Client.objects.filter(user_id=user_id).count(), 0)

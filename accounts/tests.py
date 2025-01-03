from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import (
    User, Role, Permission, RolePermission,
    UserRole, UserAddress
)
from .serializers import UserSerializer


class UserModelTests(TestCase):
    def setUp(self):
        self.user_data = {
            'telegram_id': '123456',
            'phone_number': '+1234567890',
            'email': 'test@example.com'
        }

    def test_create_user_with_telegram_id(self):
        user = User.objects.create(**self.user_data)
        self.assertTrue(user.is_telegram_user)
        self.assertEqual(user.telegram_id, '123456')
        self.assertTrue(check_password(User.DEFAULT_PASSWORD, user.password))
        self.assertEqual(user.username, user.telegram_id)

    def test_create_user_without_telegram_id(self):
        data = self.user_data.copy()
        data.pop('telegram_id')
        user = User.objects.create(**data)
        self.assertFalse(user.is_telegram_user)
        self.assertEqual(user.username, user.phone_number)


class JWTAuthenticationTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test@example.com'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.login_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')
        self.verify_url = reverse('token_verify')
        self.users_url = reverse('user-list')

    def test_obtain_token_pair(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        return response.data

    def test_refresh_token(self):
        tokens = self.test_obtain_token_pair()
        response = self.client.post(self.refresh_url, {
            'refresh': tokens['refresh']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_verify_token(self):
        tokens = self.test_obtain_token_pair()
        response = self.client.post(self.verify_url, {
            'token': tokens['access']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_token(self):
        response = self.client.post(self.verify_url, {
            'token': 'invalid_token'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_protected_endpoint_without_token(self):
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_protected_endpoint_with_token(self):
        tokens = self.test_obtain_token_pair()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_with_expired_token(self):
        tokens = self.test_obtain_token_pair()
        # Simulate expired token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'expired.token.here')
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TelegramAuthenticationTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.telegram_login_url = reverse('telegram-login')
        self.user = User.objects.create(
            username='telegramuser',
            telegram_id='123456'
        )

    def test_telegram_login_success(self):
        response = self.client.post(self.telegram_login_url, {
            'telegram_id': '123456'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_telegram_login_invalid_id(self):
        response = self.client.post(self.telegram_login_url, {
            'telegram_id': 'nonexistent'
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_telegram_token_access(self):
        # Login via telegram
        response = self.client.post(self.telegram_login_url, {
            'telegram_id': '123456'
        })
        token = response.data['access']

        # Try accessing protected endpoint
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


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
        User.objects.create(**self.user_data)
        serializer = UserSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('telegram_id', serializer.errors)


class RolePermissionTests(TestCase):
    def setUp(self):
        self.role = Role.objects.create(name='admin', description='Administrator')
        self.permission = Permission.objects.create(
            name='can_edit', 
            description='Can edit content'
        )

    def test_create_role_permission(self):
        role_perm = RolePermission.objects.create(
            role=self.role,
            permission=self.permission
        )
        self.assertEqual(str(role_perm), 'admin - can_edit')


class UserAddressTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.address = UserAddress.objects.create(
            user=self.user,
            address='123 Test St'
        )

    def test_user_address_creation(self):
        self.assertEqual(str(self.address), 'testuser - 123 Test St')
        self.assertIsNotNone(self.address.last_used_at)


class APITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username='testuser',
            telegram_id='123456',
            is_staff=True
        )
        self.client.force_authenticate(user=self.user)
        self.role = Role.objects.create(name='test_role')

    def test_user_list(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_assign_role(self):
        url = reverse('user-assign-role', kwargs={'pk': self.user.pk})
        response = self.client.post(url, {'role_id': self.role.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            UserRole.objects.filter(
                user=self.user, 
                role=self.role
            ).exists()
        )

    def test_db_connection(self):
        url = reverse('test-db')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['status'], 
            'Database connection successful'
        )

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .test_factories import UserFactory, RoleFactory, UserRoleFactory, ClientFactory
from accounts.models import (
    User, Role, Permission, RolePermission,
    UserRole, UserAddress, Client
)


class APITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory(is_staff=True)
        self.client.force_authenticate(user=self.user)
        self.role = RoleFactory()

    def test_user_list(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_assign_role(self):
        url = reverse('user-assign-role', kwargs={'pk': self.user.pk})
        response = self.client.post(url, {'role_id': self.role.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            UserRole.objects.filter(user=self.user, role=self.role).exists()
        )


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
        self.user = UserFactory(telegram_id='123456')

    def test_telegram_login_success(self):
        response = self.client.post(self.telegram_login_url, {
            'telegram_id': '123456'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


class ClientAPITests(APITestCase):
    def setUp(self):
        self.client_user = UserFactory(is_staff=True)
        self.api_client = APIClient()
        self.api_client.force_authenticate(user=self.client_user)
        self.client_instance = ClientFactory()

    def test_list_clients(self):
        url = reverse('client-list')
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_client(self):
        url = reverse('client-list')
        new_user = UserFactory()
        data = {
            'user_id': new_user.id
        }
        response = self.api_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.count(), 2)

    def test_retrieve_client(self):
        url = reverse('client-detail', kwargs={'pk': self.client_instance.pk})
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['id'], self.client_instance.user.id)

    def test_update_client(self):
        url = reverse('client-detail', kwargs={'pk': self.client_instance.pk})
        new_user = UserFactory()
        data = {
            'user_id': new_user.id
        }
        response = self.api_client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client_instance.refresh_from_db()
        self.assertEqual(self.client_instance.user.id, new_user.id)

    def test_delete_client(self):
        url = reverse('client-detail', kwargs={'pk': self.client_instance.pk})
        response = self.api_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Client.objects.count(), 0)

    def test_cannot_create_duplicate_client_for_user(self):
        url = reverse('client-list')

        # Create first client
        user = UserFactory()
        ClientFactory(user=user)

        # Try to create another client for the same user
        data = {
            'user_id': user.id
        }
        response = self.api_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user_id', response.data)

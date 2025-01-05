from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import Client
from .test_factories import UserFactory, ClientFactory


class ClientIntegrationTests(APITestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True)
        self.client.force_authenticate(user=self.user)

    def test_client_full_flow(self):
        # Create a client
        create_url = reverse('client-list')
        new_user = UserFactory()
        response = self.client.post(create_url, {'user_id': new_user.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        client_id = response.data['id']

        # Verify client was created
        detail_url = reverse('client-detail', kwargs={'pk': client_id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['id'], new_user.id)

        # Update client
        another_user = UserFactory()
        response = self.client.put(
            detail_url,
            {'user_id': another_user.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify update
        response = self.client.get(detail_url)
        self.assertEqual(response.data['user']['id'], another_user.id)

        # Delete client
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify deletion
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

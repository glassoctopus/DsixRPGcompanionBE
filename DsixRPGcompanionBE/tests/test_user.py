from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from DsixRPGcompanionBE.models import User

class UserAPITest(APITestCase):
    
    def setUp(self):
        # Initial User data
        self.user_data = {
            'uid': 'user123',
            'handle': 'test_handle',
            'bio': 'Test bio',
            'admin': False,
            'game_master': False
        }
        self.url = reverse('user-list')  # Assuming 'user-list' is the URL name for UserViewset list/create

    def test_create_user(self):
        # Create a user
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check that user was created with the correct data
        for field in self.user_data:
            self.assertEqual(response.data[field], self.user_data[field])

    def test_update_user(self):
        # Create a user
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_id = response.data['id']
        
        # Update user
        update_data = {
            'handle': 'new_handle',
            'bio': 'Updated bio',
            'admin': True,
            'game_master': True
        }
        response = self.client.put(reverse('user-detail', args=[user_id]), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify that the fields were updated
        for field in update_data:
            self.assertEqual(response.data[field], update_data[field])

    def test_get_user(self):
        # Create user
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_id = response.data['id']
        
        # Retrieve the user by ID
        response = self.client.get(reverse('user-detail', args=[user_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify retrieved data matches created data
        for field in self.user_data:
            self.assertEqual(response.data[field], self.user_data[field])


from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from DsixRPGcompanionBE.models.archetype import Archetype
from DsixRPGcompanionBE.views.archetypes import ArchetypeSerializer
from .expected_type import not_json

class ArchetypeAPITestCase(APITestCase):

    def setUp(self):
        self.archetype_data = {
            "archetype_name": "Brash Pilot",
            "archetype_personality": "Enthusiastic, loyal, energetic, and committed.",
            "archetype_background": "You thought you'd never get off that hick planet!",
            "archetype_objectives": "You want to be the best pilot in the Alliance!",
            "archetype_a_quote": "\"Heck, that flying wasn't so fancy! Back home, I used to outmaneuver XP-38s with my Mobquet landspeeder!\"",
            "archetype_force_sensitive": False,
            "archetype_dexterity": 3.0,
            "archetype_knowledge": 2.0,
            "archetype_mechanical": 4.0,
            "archetype_perception": 3.0,
            "archetype_strength": 3.0,
            "archetype_technical": 3.0,
            "archetype_force_control": 0.0,
            "archetype_force_sense": 0.0,
            "archetype_force_alter": 0.0,
            "archetype_starting_credits": 1000
        }
        self.url = reverse('archetype-list')  # Adjust if your URL pattern name is different

    def test_create_archetype(self):
        response = self.client.post(self.url, self.archetype_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #You had to do such large models and so many variable types... 
        for field, expected_value in self.archetype_data.items():
            response_value = response.data.get(field)
            if isinstance(expected_value, float):
                response_value = float(response_value)
            elif isinstance(expected_value, int):
                response_value = int(response_value)
            elif isinstance(expected_value, bool):
                response_value = response_value.lower() == 'true'
            self.assertEqual(response_value, expected_value)

    def test_get_archetype(self):
        # First create an archetype
        response = self.client.post(self.url, self.archetype_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        archetype_id = response.data['id']
        
        # Retrieve the created archetype
        response = self.client.get(reverse('archetype-detail', args=[archetype_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in self.archetype_data:
            self.assertEqual(not_json(self.archetype_data[field], response.data[field]), self.archetype_data[field])

    def test_update_archetype(self):
        # Create an archetype
        response = self.client.post(self.url, self.archetype_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        archetype_id = response.data['id']
        
        # Update the archetype
        update_data = {
            'archetype_name': 'Skilled Pilot',
            'archetype_starting_credits': 1500
        }
        response = self.client.put(reverse('archetype-detail', args=[archetype_id]), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['archetype_name'], 'Skilled Pilot')
        self.assertEqual(response.data['archetype_starting_credits'], 1500)

    def test_delete_archetype(self):
        # Create an archetype
        response = self.client.post(self.url, self.archetype_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        archetype_id = response.data['id']
        
        # Delete the archetype
        response = self.client.delete(reverse('archetype-detail', args=[archetype_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify it has been deleted
        response = self.client.get(reverse('archetype-detail', args=[archetype_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
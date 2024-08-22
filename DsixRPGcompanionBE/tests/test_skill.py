from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from DsixRPGcompanionBE.models import Skill

class SkillAPITest(APITestCase):

    def setUp(self):
        # URL for the Skill endpoint
        self.url = reverse('skill-list')

        # Data for batch creation of skills
        self.skills_data = [
            {
                "attribute": "Dexterity",
                "skill_name": "Archaic Guns",
                "time_taken": "One round",
                "is_a_reaction": False,
                "force_skill": False,
                "specializations_notes": "Indicates a specific kind or model of archaic gun",
                "modifiers": "",
                "skill_use_notes": "Archaic guns is a \"ranged combat\" skill used to fire any primitive gun",
                "skill_game_notes": "Normally, only characters from primitive-technology worlds will know this skill.",
                "skill_code": 0.0
            },
            {
                "attribute": "Dexterity",
                "skill_name": "Blaster",
                "time_taken": "One round",
                "is_a_reaction": False,
                "force_skill": False,
                "specializations_notes": "A specific type or model of character-scale blaster weapon",
                "modifiers": "",
                "skill_use_notes": "Blaster is the \"ranged combat\" skill used to shoot blaster weapons",
                "skill_game_notes": "Do not use blaster to fire fixed blasters or multicrew weapons.",
                "skill_code": 0.0
            },
            {
                "attribute": "Dexterity",
                "skill_name": "Blaster Artillery",
                "time_taken": "One round or longer",
                "is_a_reaction": False,
                "force_skill": False,
                "specializations_notes": "The particular type or model of artillery",
                "modifiers": "",
                "skill_use_notes": "Blaster artillery is the \"ranged combat\".",
                "skill_game_notes": "The time taken to use this skill is often one round",
                "skill_code": 0.0
            }
        ]

    def test_create_skill(self):
        # Create a single skill
        response = self.client.post(self.url, self.skills_data[0], format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify skill was created with correct data
        for field in self.skills_data[0]:
            self.assertEqual(response.data[field], self.skills_data[0][field])

    def test_batch_create_skills(self):
        # Batch create multiple skills
        response = self.client.post(self.url, self.skills_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Ensure response contains all created skills, need to grab them since I have a confirmation meesage in my response
        created_skills = response.data.get('created_skills', [])
        self.assertEqual(len(created_skills), len(self.skills_data))
        
        # Verify that the skills were created with the correct data
        for i, skill in enumerate(self.skills_data):
            print("(test debug)Response Data: ", response.data)
            for field in skill:
                self.assertEqual(created_skills[i][field], skill[field])

    def test_update_skill(self):
        # Create a skill first
        response = self.client.post(self.url, self.skills_data[0], format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        skill_id = response.data['id']

        # Update the skill
        update_data = {
            "attribute": "Dexterity",
            "skill_name": "Updated Archaic Guns",
            "time_taken": "Two rounds",
            "is_a_reaction": True,
            "force_skill": True,
            "specializations_notes": "Updated specializations.",
            "modifiers": "New modifiers",
            "skill_use_notes": "Updated use notes.",
            "skill_game_notes": "Updated game notes.",
            "skill_code": 1.5
        }
        response = self.client.put(reverse('skill-detail', args=[skill_id]), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify that the fields were updated
        for field in update_data:
            self.assertEqual(response.data[field], update_data[field])

    def test_get_skill(self):
        # Create a skill
        response = self.client.post(self.url, self.skills_data[0], format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        skill_id = response.data['id']

        # Retrieve the skill by ID
        response = self.client.get(reverse('skill-detail', args=[skill_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify that the retrieved data matches the created data
        for field in self.skills_data[0]:
            self.assertEqual(response.data[field], self.skills_data[0][field])

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from DsixRPGcompanionBE.models.character import Character
from DsixRPGcompanionBE.models.archetype import Archetype
from DsixRPGcompanionBE.models.user import User

class CharacterModelTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create Users
        self.user1 = User.objects.create(
            uid="user1",
            handle="user1handle",
            bio="Bio of user 1",
            admin=False,
            game_master=False
        )
        self.user2 = User.objects.create(
            uid="user2",
            handle="user2handle",
            bio="Bio of user 2",
            admin=False,
            game_master=False
        )

        # Create Archetypes
        self.archetype1 = Archetype.objects.create(
            archetype_name="Brash Pilot",
            archetype_personality="Enthusiastic, loyal, energetic, and committed.",
            archetype_background="You thought you'd never get off that hick planet!",
            archetype_objectives="You want to be the best pilot in the Alliance!",
            archetype_a_quote='"Heck, that flying wasn\'t so fancy! Back home, I used to outmaneuver XP-38s with my Mobquet landspeeder!"',
            archetype_force_sensitive=False,
            archetype_dexterity=3.0,
            archetype_knowledge=2.0,
            archetype_mechanical=4.0,
            archetype_perception=3.0,
            archetype_strength=3.0,
            archetype_technical=3.0,
            archetype_force_control=0.0,
            archetype_force_sense=0.0,
            archetype_force_alter=0.0,
            archetype_starting_credits=1000
        )
        self.archetype2 = Archetype.objects.create(
            archetype_name="Jedi knight",
            archetype_for_NPC=True,
            archetype_force_sensitive=False,
            archetype_starting_credits=0,
            archetype_game_notes="This type is for prototyping, or Game Masters"
        )
        self.archetype3 = Archetype.objects.create(
            archetype_name="Jedi Master",
            archetype_for_NPC=True,
            archetype_force_sensitive=False,
            archetype_starting_credits=0,
            archetype_game_notes="This type is for prototyping, or Game Masters"
        )

        # Create Characters
        self.character_data = [
            { 
                "uid": "whiny_Luke",
                "NPC": False,
                "user": self.user1.id,
                "image": "image_url_here",
                "name": "Luke Skywalker",
                "archetype": self.archetype1.id,
                "species": "Human",
                "homeworld": "Tatooine",
                "gender": "Male",
                "age": 19,
                "height": "172 cm",
                "weight": "77 kg",
                "physical_description": "Blonde hair, blue eyes, athletic build.",
                "personality": "Idealistic, determined, strong sense of duty.",
                "background": "Moisture farmer on Tatooine, orphaned, raised by Uncle Owen and Aunt Beru.",
                "objectives": "To become a Jedi and defeat the Empire.",
                "a_quote": "I'm Luke Skywalker. I'm here to rescue you.",
                "credits": 1000,
                "force_sensitive": True,
                "dexterity": 3.0,
                "knowledge": 2.0,
                "mechanical": 3.5,
                "perception": 2.1,
                "strength": 3.0,
                "technical": 3.0,
                "force_control": 3.0,
                "force_sense": 2.0,
                "force_alter": 0.0,
                "force_points": 6.0,
                "dark_side_points": 0.0,
                "force_strength": 0.0
            },
            { 
                "uid": "better_Luke",
                "NPC": False,
                "user": self.user1.id,
                "image": "image_url_here",
                "name": "Luke Skywalker",
                "archetype": self.archetype2.id,
                "species": "Human",
                "homeworld": "Tatooine",
                "gender": "Male",
                "age": 22,
                "height": "172 cm",
                "weight": "77 kg",
                "physical_description": "Blonde hair, blue eyes, athletic build, more mature.",
                "personality": "Determined, focused, more confident as a leader.",
                "background": "Trained by Obi-Wan and Yoda, fought in the Battle of Hoth.",
                "objectives": "To defeat the Empire and become a Jedi Knight.",
                "a_quote": "I won't fail you. I'm not afraid.",
                "credits": 1500,
                "force_sensitive": True,
                "dexterity": 3.0,
                "knowledge": 2.0,
                "mechanical": 4.0,
                "perception": 2.1,
                "strength": 3.0,
                "technical": 3.0,
                "force_control": 9.0,
                "force_sense": 7.0,
                "force_alter": 6.0,
                "force_points": 12.0,
                "dark_side_points": 0.0,
                "force_strength": 0.0
            },
            { 
                "uid": "Jedi_Luke",
                "NPC": False,
                "user": self.user2.id,
                "image": "image_url_here",
                "name": "Luke Skywalker",
                "archetype": self.archetype3.id,
                "species": "Human",
                "homeworld": "Tatooine",
                "gender": "Male",
                "age": 23,
                "height": "172 cm",
                "weight": "77 kg",
                "physical_description": "Blonde hair, blue eyes, athletic build, confident.",
                "personality": "Calm, confident, strong moral code.",
                "background": "Trained further by Yoda, helped defeat the Empire.",
                "objectives": "To bring balance to the Force and redeem his father.",
                "a_quote": "I am a Jedi, like my father before me.",
                "credits": 2000,
                "force_sensitive": True,
                "dexterity": 3.0,
                "knowledge": 2.0,
                "mechanical": 4.0,
                "perception": 3.0,
                "strength": 3.0,
                "technical": 3.0,
                "force_control": 13.0,
                "force_sense": 10.0,
                "force_alter": 9.0,
                "force_points": 16.0,
                "dark_side_points": 0.0,
                "force_strength": 0.0
            },
            { 
                "uid": "DE_Luke",
                "NPC": False,
                "user": self.user1.id,
                "image": "image_url_here",
                "name": "Luke Skywalker",
                "archetype": self.archetype2.id,
                "species": "Human",
                "homeworld": "Tatooine",
                "gender": "Male",
                "age": 28,
                "height": "172 cm",
                "weight": "77 kg",
                "physical_description": "Blonde hair, blue eyes, athletic build, darker and more brooding.",
                "personality": "Conflicted, struggling with the pull of the Dark Side, determined.",
                "background": "Turned to the Dark Side in an attempt to destroy it from within.",
                "objectives": "To learn the secrets of the Dark Side and ultimately destroy it.",
                "a_quote": "The Dark Side is strong, but I will find a way to defeat it.",
                "credits": 2500,
                "force_sensitive": True,
                "dexterity": 3.5,
                "knowledge": 3.0,
                "mechanical": 4.0,
                "perception": 3.0,
                "strength": 3.0,
                "technical": 3.5,
                "force_control": 15.0,
                "force_sense": 12.0,
                "force_alter": 10.0,
                "force_points": 18.0,
                "dark_side_points": 8.0,
                "force_strength": 0.0
            }
        ]

    def test_create_character(self):
        response = self.client.post(reverse('hero-list'), self.character_data[0], format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Character.objects.count(), 1)
        self.assertEqual(Character.objects.get().uid, 'whiny_Luke')

    def test_list_characters(self):
        for data in self.character_data:
            self.client.post(reverse('hero-list'), data, format='json')
        response = self.client.get(reverse('hero-list'))
        response_data = response.data
        heros = response_data['They are']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(heros), 4)

    def test_update_character(self):
        self.client.post(reverse('hero-list'), self.character_data[0], format='json')
        character = Character.objects.get(uid='whiny_Luke')
        update_data = {
            "uid": "whiny_Luke",
            "NPC": False,
            "user": self.user1.id,
            "image": "new_image_url_here",
            "name": "Luke Skywalker Updated",
            "archetype": self.archetype1.id,
            "species": "Human",
            "homeworld": "Tatooine",
            "gender": "Male",
            "age": 20,
            "height": "172 cm",
            "weight": "77 kg",
            "physical_description": "Updated description.",
            "personality": "Updated personality.",
            "background": "Updated background.",
            "objectives": "Updated objectives.",
            "a_quote": "Updated quote.",
            "credits": 1500,
            "force_sensitive": True,
            "dexterity": 4.0,
            "knowledge": 3.0,
            "mechanical": 4.5,
            "perception": 3.2,
            "strength": 3.5,
            "technical": 3.5,
            "force_control": 4.0,
            "force_sense": 3.0,
            "force_alter": 1.0,
            "force_points": 8.0,
            "dark_side_points": 0.0,
            "force_strength": 0.0
        }
        response = self.client.put(reverse('hero-detail', args=[character.id]), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Character.objects.get(uid='whiny_Luke').name, 'Luke Skywalker Updated')

    def test_delete_character(self):
        self.client.post(reverse('hero-list'), self.character_data[0], format='json')
        character = Character.objects.get(uid='whiny_Luke')
        response = self.client.delete(reverse('hero-detail', args=[character.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Character.objects.count(), 0)
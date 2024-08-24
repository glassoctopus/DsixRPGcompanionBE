from rest_framework import status
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from DsixRPGcompanionBE.models.character_group import CharacterGroup
from DsixRPGcompanionBE.models.character import Character
from DsixRPGcompanionBE.models.user import User

class CharacterGroupCRUDTestCase(TestCase):

    def setUp(self):
        # Create test users
        self.user1 = User.objects.create(handle='player1')
        self.user2 = User.objects.create(handle='player2')

        # Create test characters
        self.character1 = Character.objects.create(name='Character 1', uid='char1', user=self.user1)
        self.character2 = Character.objects.create(name='Character 2', uid='char2', user=self.user1)

    def test_create_character_group(self):
        """Test creating a character group"""
        group = CharacterGroup.objects.create(
            user=self.user1,
            group_name="Test Group",
            is_adventure_party=False
        )
        self.assertEqual(group.group_name, "Test Group")
        self.assertEqual(group.user, self.user1)
        self.assertFalse(group.is_adventure_party)

    def test_retrieve_character_group(self):
        """Test retrieving a character group"""
        group = CharacterGroup.objects.create(
            user=self.user1,
            group_name="Test Group",
            is_adventure_party=False
        )
        retrieved_group = CharacterGroup.objects.get(id=group.id)
        self.assertEqual(retrieved_group.group_name, "Test Group")
        self.assertEqual(retrieved_group.user, self.user1)

    def test_update_character_group(self):
        """Test updating a character group"""
        group = CharacterGroup.objects.create(
            user=self.user1,
            group_name="Test Group",
            is_adventure_party=False
        )
        # Update the group
        group.group_name = "Updated Group"
        group.game_master = self.user1
        group.is_adventure_party = True
        group.save()

        updated_group = CharacterGroup.objects.get(id=group.id)
        self.assertEqual(updated_group.group_name, "Updated Group")
        self.assertTrue(updated_group.is_adventure_party)

    def test_delete_character_group(self):
        """Test deleting a character group"""
        group = CharacterGroup.objects.create(
            user=self.user1,
            group_name="Test Group",
            is_adventure_party=False
        )
        group_id = group.id
        group.delete()

        with self.assertRaises(CharacterGroup.DoesNotExist):
            CharacterGroup.objects.get(id=group_id)

    def test_add_characters_to_group(self):
        """Test adding characters to a character group"""
        group = CharacterGroup.objects.create(
            user=self.user1,
            group_name="Test Group",
            is_adventure_party=False
        )
        
        # Add characters to the group
        group.characters.add(self.character1, self.character2)
        group.save()

        # Ensure characters are added to the group
        self.assertEqual(group.characters.count(), 2)
        self.assertIn(self.character1, group.characters.all())
        self.assertIn(self.character2, group.characters.all())

    def test_create_public_adventure_party_without_game_master(self):
        """Test creating a public adventure party without a game master should raise ValidationError"""
        group = CharacterGroup(
            user=self.user1,
            group_name="Adventure Party",
            is_adventure_party=True,
            private=False
        )
        
        with self.assertRaises(ValidationError):
            group.clean()  # Should raise ValidationError because no game master is set

    def test_create_public_adventure_party_with_game_master(self):
        """Test creating a public adventure party with a game master should succeed"""
        group = CharacterGroup(
            user=self.user1,
            group_name="Adventure Party",
            is_adventure_party=True,
            private=False,
            game_master=self.user2
        )
        
        try:
            group.clean()  # Should pass validation
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly for public adventure party with game master!")



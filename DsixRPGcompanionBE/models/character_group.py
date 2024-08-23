from django.db import models
from django.core.exceptions import ValidationError
from .character import Character
from .user import User

class CharacterGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_groups')
    group_name = models.CharField(max_length=69)
    game_master = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='gm_groups')
    characters = models.ManyToManyField(Character, blank=True, related_name='chatacter_groups')
    private = models.BooleanField(default=False)
    is_adventure_party = models.BooleanField(default=False)

    def __str__(self):
        return self.group_name

    def clean(self):
        # If the group is an adventure party, it must have a game master
        if not self.private and self.is_adventure_party and not self.game_master:
            raise ValidationError("A public adventure party must have a game master.")

        # If the group is private, having a game master is optional
        if self.private and self.is_adventure_party and self.game_master:
            if not self.users.filter(id=self.game_master.id, game_master=True).exists():
                raise ValidationError("group is private, for the user only")

        # Ensure only one user is set as the game master for the group
        if self.game_master and not self.users.filter(id=self.game_master.id).exists():
            raise ValidationError("Only a single user with the game master flag set, must be part of an Adventure user group.")

    def save(self, *args, **kwargs):
        from .user import User  # Import the User model here
        self.clean()  # Call the clean method for validation
        super(CharacterGroup, self).save(*args, **kwargs)
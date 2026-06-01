from django.db import models
from .archetype import Archetype
from .species import Species
from .skill import Skill
from .user import User

class Character(models.Model):
    uid = models.CharField(max_length=113, unique=True)
    NPC = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='characters', null=True, blank=True)
    image = models.CharField(max_length=223, null=True, blank=True)
    name = models.CharField(max_length=69, null=True, blank=True)
    archetype = models.ForeignKey(Archetype, on_delete=models.CASCADE, related_name='archetypes', null=True, blank=True)
    species = models.ForeignKey(Species, on_delete=models.CASCADE, related_name='characters', null=True, blank=True)
    homeworld = models.CharField(max_length=69, null=True, blank=True)
    gender = models.CharField(max_length=13, null=True, blank=True)
    age = models.IntegerField(default=21, null=True, blank=True)
    height = models.CharField(max_length=13, null=True, blank=True)
    weight = models.CharField(max_length=13, null=True, blank=True)
    force_sensitive = models.BooleanField(default=False, null=True, blank=True)
    dexterity = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    knowledge = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    mechanical = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    perception = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    strength = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    technical = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    force_control = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    force_sense = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    force_alter = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    force_points = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    dark_side_points = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    physical_description = models.CharField(max_length=2369, null=True, blank=True)
    personality = models.CharField(max_length=2369, null=True, blank=True)
    background = models.CharField(max_length=2369, null=True, blank=True)
    objectives = models.CharField(max_length=2369, null=True, blank=True)
    a_quote = models.CharField(max_length=2369, null=True, blank=True)
    credits = models.IntegerField(default=0, null=True, blank=True)
    force_strength = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    skill_points = models.IntegerField(default=0, null=True, blank=True)
    skills = models.ManyToManyField(Skill, through='CharacterSkill')
    
    def __str__(self):
        return self.name

    def character_header(self):
        return f"{self.name} (UID: {self.uid}, Handle: {self.user_handle if self.user else 'No User'})"

    @property
    def user_handle(self):
        return self.user.handle if self.user else 'No User'
    
    @property
    def archetype_name(self):
        return self.archetype.archetype_name if self.archetype else 'No Archetype'
    
    @property
    def species_name(self):
        return self.species.species_name if self.species else 'No Species'
    
    def can_equip_item(self, equipment):
        """Check if character meets all requirements for equipment"""
        # Check archetype restrictions
        if equipment.required_archetypes.exists():
            if self.archetype not in equipment.required_archetypes.all():
                # Check for override
                if not EquipmentRestrictionOverride.objects.filter(
                    character=self, equipment=equipment, can_equip=True
                ).exists():
                    return False, f"Requires archetype: {', '.join([a.archetype_name for a in equipment.required_archetypes.all()])}"
        
        if equipment.prohibited_archetypes.exists():
            if self.archetype in equipment.prohibited_archetypes.all():
                return False, f"Prohibited for {self.archetype.archetype_name} archetype"
        
        # Check species restrictions
        if equipment.required_species.exists():
            if self.species not in equipment.required_species.all():
                if not EquipmentRestrictionOverride.objects.filter(
                    character=self, equipment=equipment, can_equip=True
                ).exists():
                    return False, f"Requires species: {', '.join([s.species_name for s in equipment.required_species.all()])}"
        
        if equipment.prohibited_species.exists():
            if self.species in equipment.prohibited_species.all():
                return False, f"Prohibited for {self.species.species_name} species"
        
        # Check skill requirement
        if equipment.required_skill and equipment.required_skill_rank:
            try:
                char_skill = CharacterSkill.objects.get(
                    character=self, 
                    skill=equipment.required_skill
                )
                if char_skill.skill_code < equipment.required_skill_rank:
                    return False, f"Requires {equipment.required_skill.skill_name} at {equipment.required_skill_rank}D"
            except CharacterSkill.DoesNotExist:
                return False, f"Requires {equipment.required_skill.skill_name} at {equipment.required_skill_rank}D"
        
        return True, "Can equip"
    
    def get_total_encumbrance(self):
        """Calculate total weight of carried/equipped items"""
        total_weight = 0
        inv_items = self.inventory.filter(status__in=['carried', 'equipped'])
        for item in inv_items:
            if item.equipment.weight_kg:
                total_weight += item.equipment.weight_kg * item.quantity
        return total_weight
    
    def get_equipped_weapons(self):
        return self.equipped_weapons.select_related('character_equipment__equipment').all()
    
    def get_equipped_armor(self):
        return getattr(self, 'equipped_armor', None)
    
    def get_equipped_gear(self):
        return self.equipped_gear.select_related('character_equipment__equipment').all()
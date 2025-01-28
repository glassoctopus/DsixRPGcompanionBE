from rest_framework import serializers
from DsixRPGcompanionBE.models import Species, Ability, Skill

class AbilityField(serializers.PrimaryKeyRelatedField):
    queryset = Ability.objects.all()

    def to_internal_value(self, data):
        if isinstance(data, dict):  # If a dict is provided, check or create the Ability
            ability_name = data.get("ability_name")
            if ability_name:
                ability, created = Ability.objects.get_or_create(ability_name=ability_name, defaults=data)
                return ability
            raise serializers.ValidationError("Ability dictionary must include 'ability_name'.")
        elif isinstance(data, int):  # If an ID is provided, validate it
            try:
                return Ability.objects.get(pk=data)
            except Ability.DoesNotExist:
                raise serializers.ValidationError(f"Ability with ID {data} does not exist.")
        raise serializers.ValidationError("Invalid data for Ability. Expected a dictionary or integer.")

    def to_representation(self, value):
        return {"id": value.id, "ability_name": value.ability_name}


class SkillField(serializers.PrimaryKeyRelatedField):
    queryset = Skill.objects.all()

    def to_internal_value(self, data):
        if isinstance(data, dict):  # If a dict is provided, check or create the Skill
            skill_name = data.get("skill_name")
            if skill_name:
                skill, created = Skill.objects.get_or_create(skill_name=skill_name, defaults=data)
                return skill
            raise serializers.ValidationError("Skill dictionary must include 'skill_name'.")
        elif isinstance(data, int):  # If an ID is provided, validate it
            try:
                return Skill.objects.get(pk=data)
            except Skill.DoesNotExist:
                raise serializers.ValidationError(f"Skill with ID {data} does not exist.")
        raise serializers.ValidationError("Invalid data for Skill. Expected a dictionary or integer.")

    def to_representation(self, value):
        return {"id": value.id, "skill_name": value.skill_name}


class SpeciesSerializer(serializers.ModelSerializer):
    species_abilities = AbilityField(many=True, required=False)
    species_skills = SkillField(many=True, required=False)

    class Meta:
        model = Species
        fields = (
            'id',
            'uid',
            'playable',
            'image',
            'species_name',
            'species_homeworld',
            'species_average_height',
            'species_average_weight',
            'species_force_sensitive',
            'species_dexterity',
            'species_knowledge',
            'species_mechanical',
            'species_perception',
            'species_strength',
            'species_technical',
            'species_force_control',
            'species_force_sense',
            'species_force_alter',
            'species_force_points',
            'species_dark_side_points',
            'species_abilities',
            'species_skills',
            'species_physical_description',
            'species_personality',
            'species_background',
            'species_force_strength',
            'species_appeared_in',
        )

    def create(self, validated_data):
        abilities_data = validated_data.pop('species_abilities', [])
        skills_data = validated_data.pop('species_skills', [])

        # Lazy imports here to avoid circular dependency during the initial loading phase
        from DsixRPGcompanionBE.serializers.ability import AbilitySerializer
        from DsixRPGcompanionBE.serializers.skill import SkillSerializer

        species = Species.objects.create(**validated_data) # like gawd, created a whole species

        for ability_data in abilities_data:
            if isinstance(ability_data, Ability): #single ability
                ability_name = ability_data.ability_name
                ability, created = Ability.objects.get_or_create(
                    ability_name=ability_name, defaults={'ability_name': ability_name}
                )
                ability.species = species #assign it to the speices just created
                ability.save()
            else: #dict of abilites
                ability_name = ability_data.get('ability_name')
                if ability_name:
                    ability, created = Ability.objects.get_or_create(
                        ability_name=ability_name, defaults=ability_data
                    )
                    ability.species = species
                    ability.save()

        for skill_data in skills_data:
            if isinstance(skill_data, Skill):
                skill_name = skill_data.skill_name
                skill, created = Skill.objects.get_or_create(
                    skill_name=skill_name, defaults={'skill_name': skill_name}
                )
                skill.species = species
                skill.save()
            else:
                skill_name = skill_data.get('skill_name')
                if skill_name:
                    skill, created = Skill.objects.get_or_create(
                        skill_name=skill_name, defaults=skill_data
                    )
                    skill.species = species
                    skill.save()

        return species

    def update(self, instance, validated_data):
        abilities_data = validated_data.pop('species_abilities', None)
        skills_data = validated_data.pop('species_skills', None)

        # Lazy imports here to avoid circular dependency during the initial loading phase
        from DsixRPGcompanionBE.serializers.ability import AbilitySerializer
        from DsixRPGcompanionBE.serializers.skill import SkillSerializer

        if abilities_data is not None:
            instance.species_abilities.clear()  
            for ability_data in abilities_data:
                if isinstance(ability_data, Ability):
                    ability_name = ability_data.ability_name
                    ability, created = Ability.objects.get_or_create(
                        ability_name=ability_name, defaults={'ability_name': ability_name}
                    )
                    ability.species = instance
                    ability.save()
                else:
                    ability_name = ability_data.get('ability_name')
                    if ability_name:
                        ability, created = Ability.objects.get_or_create(
                            ability_name=ability_name, defaults=ability_data
                        )
                        ability.species = instance
                        ability.save()

        if skills_data is not None:
            instance.species_skills.clear()
            for skill_data in skills_data:
                if isinstance(skill_data, Skill):
                    skill_name = skill_data.skill_name
                    skill, created = Skill.objects.get_or_create(
                        skill_name=skill_name, defaults={'skill_name': skill_name}
                    )
                    skill.species = instance
                    skill.save()
                else:
                    skill_name = skill_data.get('skill_name')
                    if skill_name:
                        skill, created = Skill.objects.get_or_create(
                            skill_name=skill_name, defaults=skill_data
                        )
                        skill.species = instance
                        skill.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


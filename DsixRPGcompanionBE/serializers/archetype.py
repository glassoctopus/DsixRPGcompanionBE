from rest_framework import serializers
from DsixRPGcompanionBE.models.archetype import Archetype
from DsixRPGcompanionBE.models.species import Species

# TODO
# class ArchetypeEquipmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ArchetypeEquipment
#         fields = ('id', 'archetype', 'equipment', 'quantity')

class SpeciesField(serializers.PrimaryKeyRelatedField):
    queryset = Species.objects.all() 
    
    def to_internal_value(self, data):
        if isinstance(data, str):  # if data is a string (species name)
            species_obj, created = Species.objects.get_or_create(species_name=data)
            return species_obj
        elif isinstance(data, int):  # if data is an integer (primary key)
            return super().to_internal_value(data)
        elif isinstance(data, Species):  # if data is an actual Species object
            return data
        raise serializers.ValidationError("Invalid species data. It must be a string (species name), int (species id), or Species object.")
    
    def to_representation(self, value):
        return value.species_name  # represent as species name

class ArchetypeSerializer(serializers.ModelSerializer):
    # archetype_equipment = ArchetypeEquipmentSerializer(many=True, required=False)
    archetype_dexterity = serializers.DecimalField(max_digits=3, decimal_places=1)
    archetype_knowledge = serializers.DecimalField(max_digits=3, decimal_places=1)
    archetype_mechanical = serializers.DecimalField(max_digits=3, decimal_places=1)
    archetype_perception = serializers.DecimalField(max_digits=3, decimal_places=1)
    archetype_strength = serializers.DecimalField(max_digits=3, decimal_places=1)
    archetype_technical = serializers.DecimalField(max_digits=3, decimal_places=1)
    archetype_force_control = serializers.DecimalField(max_digits=3, decimal_places=1)
    archetype_force_sense = serializers.DecimalField(max_digits=3, decimal_places=1)
    archetype_force_alter = serializers.DecimalField(max_digits=3, decimal_places=1)
    archetype_allowed_species = SpeciesField(many=True, required=False)

    class Meta:
        model = Archetype
        fields = ('id', 
                  'archetype_name', 
                  'archetype_for_NPC', 
                  'archetype_force_sensitive', 
                  'archetype_dexterity', 
                  'archetype_knowledge', 
                  'archetype_mechanical', 
                  'archetype_perception', 
                  'archetype_strength', 
                  'archetype_technical', 
                  'archetype_force_control', 
                  'archetype_force_sense', 
                  'archetype_force_alter', 
                  'archetype_starting_credits', 
                  'archetype_personality', 
                  'archetype_background', 
                  'archetype_objectives', 
                  'archetype_a_quote',
                  'archetype_allowed_species', 
                  'archetype_game_notes', 
                  'archetype_source')
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.archetype_allowed_species.exists():
            representation['archetype_allowed_species'] = [species.species_name for species in instance.archetype_allowed_species.all()]
            
        filtered_representation = {key: value for key, value in representation.items() if value not in [None, '', {}]}
        return filtered_representation
        
    def create(self, validated_data):
        # equipment_list = validated_data.pop('archetype_equipment', [])
        allowed_species = validated_data.pop('archetype_allowed_species', [])
        archetype = Archetype.objects.create(**validated_data)
        
        resolved_species = []
        for species in allowed_species:
            if isinstance(species, Species):
                resolved_species.append(species)
            elif isinstance(species, int):
                species_obj = Species.objects.get(pk=species)
                resolved_species.append(species_obj)
            elif isinstance(species, str):
                species_obj, created = Species.objects.get_or_create(species_name=species)
                resolved_species.append(species_obj)
            
        archetype.archetype_allowed_species.set(resolved_species)
        # for piece in equipment_list:
        #     ArchetypeEquipment.objects.create(archetype=archetype, **piece)
        return archetype
    
    def update(self, instance, validated_data):
        allowed_species_data = validated_data.pop('archetype_allowed_species', None)
        if allowed_species_data is not None:
            resolved_species = []
            for species in allowed_species_data:
                if isinstance(species, Species):
                    resolved_species.append(species)
                elif isinstance(species, int):
                    species_obj = Species.objects.get(pk=species)
                    resolved_species.append(species_obj)
                elif isinstance(species, str):
                    species_obj, created = Species.objects.get_or_create(species_name=species)
                    resolved_species.append(species_obj)            
            instance.archetype_allowed_species.set(resolved_species)
            
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()
        return instance
        
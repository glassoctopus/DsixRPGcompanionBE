from rest_framework import serializers
from DsixRPGcompanionBE.models.archetype import Archetype
from DsixRPGcompanionBE.models.species import Species
import uuid

# TODO
# class ArchetypeEquipmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ArchetypeEquipment
#         fields = ('id', 'archetype', 'equipment', 'quantity')

class SpeciesField(serializers.PrimaryKeyRelatedField):
    queryset = Species.objects.all()

    def to_internal_value(self, data):
        if data is None:
            return None

        if isinstance(data, list):
            resolved_species = []
            for item in data:
                resolved_species.append(self.process_species(item))
            return resolved_species
        
        return self.process_species(data)

    def process_species(self, item):
        if isinstance(item, str):  # if item is a string (species name)
            try:
                species_obj = Species.objects.get(species_name=item)
            except Species.DoesNotExist:
                species_obj = Species(species_name=item, uid=uuid.uuid4())
                species_obj.save()
            return species_obj
        elif isinstance(item, int):  # if item is an integer (primary key)
            return item
        elif isinstance(item, Species):  # if item is an actual Species object
            return item.pk
        raise serializers.ValidationError("Invalid species data. It must be a string (species name), int (species id), or Species object.")

    def to_representation(self, value):
        if isinstance(value, list):
            return [species.species_name for species in value]
        return value.species_name


class ArchetypeSerializer(serializers.ModelSerializer):
    # equipment = ArchetypeEquipmentSerializer(many=True, required=False)
    dexterity = serializers.DecimalField(max_digits=3, decimal_places=1)
    knowledge = serializers.DecimalField(max_digits=3, decimal_places=1)
    mechanical = serializers.DecimalField(max_digits=3, decimal_places=1)
    perception = serializers.DecimalField(max_digits=3, decimal_places=1)
    strength = serializers.DecimalField(max_digits=3, decimal_places=1)
    technical = serializers.DecimalField(max_digits=3, decimal_places=1)
    force_control = serializers.DecimalField(max_digits=3, decimal_places=1)
    force_sense = serializers.DecimalField(max_digits=3, decimal_places=1)
    force_alter = serializers.DecimalField(max_digits=3, decimal_places=1)
    allowed_species = SpeciesField(many=True, required=False)

    class Meta:
        model = Archetype
        fields = ('id', 
                  'name', 
                  'for_NPC', 
                  'force_sensitive', 
                  'dexterity', 
                  'knowledge', 
                  'mechanical', 
                  'perception', 
                  'strength', 
                  'technical', 
                  'force_control', 
                  'force_sense', 
                  'force_alter', 
                  'starting_credits', 
                  'personality', 
                  'background', 
                  'objectives', 
                  'a_quote',
                  'allowed_species', 
                  'game_notes', 
                  'source')
            
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.allowed_species.exists():
            representation['allowed_species'] = [species.species_name for species in instance.allowed_species.all()]
            
        filtered_representation = {key: value for key, value in representation.items() if value not in [None, '', {}]}
        return filtered_representation
        
    def create(self, validated_data):
        # equipment_list = validated_data.pop('equipment', [])
        allowed_species = validated_data.pop('allowed_species', [])
        archetype = Archetype.objects.create(**validated_data)        
        archetype.allowed_species.set(allowed_species)
        # for piece in equipment_list:
        #     ArchetypeEquipment.objects.create(archetype=archetype, **piece)
        return archetype
    
    def update(self, instance, validated_data):
        allowed_species_data = validated_data.pop('allowed_species', None)
        if allowed_species_data is not None:     
            instance.allowed_species.set(allowed_species_data)
            
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()
        return instance
        
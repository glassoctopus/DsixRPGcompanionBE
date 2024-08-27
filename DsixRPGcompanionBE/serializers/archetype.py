from rest_framework import serializers
from DsixRPGcompanionBE.models.archetype import Archetype

# TODO
# class ArchetypeEquipmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ArchetypeEquipment
#         fields = ('id', 'archetype', 'equipment', 'quantity')

class ArchetypeSerializer(serializers.ModelSerializer):
    # archetype_equipment = ArchetypeEquipmentSerializer(many=True, required=False)

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
                  'archetype_game_notes', 
                  'archetype_source')
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        filtered_representation = {key: value for key, value in representation.items() if value not in [None, '', {}]}
        return filtered_representation
        
    def create(self, validated_data):
        # equipment_list = validated_data.pop('archetype_equipment', [])
        archetype = Archetype.objects.create(**validated_data)
        # for piece in equipment_list:
        #     ArchetypeEquipment.objects.create(archetype=archetype, **piece)
        return archetype
from rest_framework import serializers, status
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
        fields = ('id', 'archetype_name', 'archetype_force_sensitive', 'archetype_dexterity', 'archetype_knowledge', 'archetype_mechanical', 'archetype_perception', 'archetype_strength', 'archetype_technical', 'archetype_force_control', 'archetype_force_sense', 'archetype_force_alter', 'archetype_starting_credits', 'archetype_personality', 'archetype_background', 'archetype_objectives', 'archetype_a_quote',)
        
    def create(self, validated_data):
        # equipment_list = validated_data.pop('archetype_equipment', [])
        archetype = Archetype.objects.create(**validated_data)
        # for piece in equipment_list:
        #     ArchetypeEquipment.objects.create(archetype=archetype, **piece)
        return archetype
from django.utils import timezone
from rest_framework import serializers
from DsixRPGcompanionBE.models import User

class UserSerializer(serializers.ModelSerializer):
    # Make password write-only and required only for creation
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'bio',
            'game_master',
            'game_master_requested',
            'game_master_approved',
            'game_master_requested_at',
            'game_master_request_to',
            'game_master_approved_by',
            'is_staff',
            'is_superuser',
            'password',
        )
        read_only_fields = ('id', 'game_master_requested_at')
        extra_kwargs = {
            'game_master_request_to': {'required': False, 'allow_null': True},
            'game_master_approved_by': {'required': False, 'allow_null': True},
            'is_superuser': {'required': False},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)   # hashes automatically
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
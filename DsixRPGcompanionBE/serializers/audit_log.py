from rest_framework import serializers
from DsixRPGcompanionBE.models.audit_log import AuditLog

class AuditLogSerializer(serializers.ModelSerializer):
    source_label = serializers.CharField(source='get_source_type_display', read_only=True)
    action_label = serializers.CharField(source='get_action_display', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True, default=None)
    timestamp = serializers.DateTimeField(format='%Y-%m-%d')
    class Meta:
        model = AuditLog
        fields = [
            'id',
            'source_type',
            'source_label',
            'payload_type',
            'payload_label',
            'action',
            'action_label',
            'user',
            'user_username',
            'timestamp',
            'request_meta',
            'old_data',
            'new_data',
        ]
        read_only_fields = ['id', 'source_type', 'payload_type', 'action', 'user', 'timestamp', 'request_meta', 'old_data', 'new_data']
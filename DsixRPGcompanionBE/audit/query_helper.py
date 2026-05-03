from models.audit_log import AuditLog
from django.contrib.contenttypes.models import ContentType

class AuditQueryHelper:
    @staticmethod
    def get_creator(obj):
        """Returns who created this object"""
        from models.audit_log import AuditLog
        log = AuditLog.objects.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk,
            action='CREATE'
        ).first()
        
        if not log:
            return None, 'unknown'
        
        if log.source_type == AuditLog.SourceType.USER and log.user:
            return log.user, 'user'
        
        return log.get_source_type_display(), log.source_type
    
    @staticmethod
    def get_audit_history(obj):
        """Full audit trail for an object"""
        return AuditLog.objects.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk
        ).order_by('-timestamp')
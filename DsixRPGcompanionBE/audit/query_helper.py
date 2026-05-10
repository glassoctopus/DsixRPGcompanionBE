from DsixRPGcompanionBE.models.audit_log import AuditLog
from django.contrib.contenttypes.models import ContentType

class AuditQueryHelper:
    @staticmethod
    def get_creator(obj):
        """Returns who created this object"""
        print(f"\n=== get_creator called for {obj.__class__.__name__} id={obj.pk} ===")
        
        log = AuditLog.objects.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk,
            action='CREATE'
        ).first()
        
        print(f"Found audit log: {log}")
        
        if not log:
            print("No CREATE audit log found")
            return None, 'unknown'
        
        print(f"log.source_type = {log.source_type}")
        print(f"log.source_type value = {getattr(log, 'source_type', 'NOT SET')}")
        print(f"log.user = {log.user}")
        print(f"log.user_id = {log.user_id}")
        print(f"log.action = {log.action}")
        print(f"log.timestamp = {log.timestamp}")
        print(f"log.old_data = {log.old_data}")
        print(f"log.new_data = {log.new_data}")
        print(f"log.request_meta = {log.request_meta}")
        
        # Check what fields actually exist
        print(f"\nAll fields in this audit log:")
        for field in log._meta.fields:
            print(f"  {field.name} = {getattr(log, field.name, 'NOT SET')}")
        
        if log.source_type == AuditLog.SourceType.USER and log.user:
            print("Returning: (log.user, 'user')")
            return log.user, 'user'
        
        print(f"Returning: (log.get_source_type_display(), log.source_type)")
        return log.get_source_type_display(), log.source_type
    
    @staticmethod
    def get_audit_history(obj):
        """Full audit trail for an object"""
        print(f"\n=== get_audit_history called for {obj.__class__.__name__} id={obj.pk} ===")
        
        logs = AuditLog.objects.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk
        ).order_by('-timestamp')
        
        print(f"Found {logs.count()} audit logs")
        
        for i, log in enumerate(logs):
            print(f"\n--- Log {i+1} ---")
            print(f"  action: {log.action}")
            print(f"  source_type: {log.source_type}")
            print(f"  user: {log.user}")
            print(f"  timestamp: {log.timestamp}")
            print(f"  old_data keys: {list(log.old_data.keys()) if log.old_data else 'None'}")
            print(f"  new_data keys: {list(log.new_data.keys()) if log.new_data else 'None'}")
        
        return logs
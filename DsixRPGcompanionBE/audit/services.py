from django.contrib.contenttypes.models import ContentType
from DsixRPGcompanionBE.models.audit_log import AuditLog
from DsixRPGcompanionBE.audit.middleware import AuditContext
from decimal import Decimal
import json
from django.core.serializers.json import DjangoJSONEncoder

class AuditService:
    @staticmethod
    def log(action, content_object, request=None, old_data=None, new_data=None):
        source_type = AuditContext.get_source_type(request)
        
        # Convert Decimal to float or string for JSON serialization
        old_data_serialized = AuditService._serialize_data(old_data)
        new_data_serialized = AuditService._serialize_data(new_data)
        
        # Create a NEW row for each change (preserves full history)
        audit_log = AuditLog(
            content_object=content_object,
            action=action.lower(),
            source_type=source_type,
            user=request.user if request and request.user.is_authenticated else None,
            request_meta={
                'ip': AuditService._get_client_ip(request),
                'user_agent': request.META.get('HTTP_USER_AGENT', '') if request else '',
                'path': request.path if request else '',
                'method': request.method if request else '',
            } if request else {},
            old_data=old_data_serialized,
            new_data=new_data_serialized,
        )
        audit_log.save()
    
    @staticmethod
    def _serialize_data(data):
        """Convert non-JSON-serializable data (like Decimal) to JSON-safe types"""
        if data is None:
            return None
        
        # Use Django's JSON encoder which handles Decimal, datetime, etc.
        return json.loads(json.dumps(data, cls=DjangoJSONEncoder))
    
    @staticmethod
    def _get_client_ip(request):
        if not request:
            return None
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

from threading import local
from DsixRPGcompanionBE.models.audit_log import AuditLog

_audit_local = local()

class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Store request context for later use
        _audit_local.request = request
        response = self.get_response(request)
        return response
    
    @staticmethod
    def get_current_request():
        return getattr(_audit_local, 'request', None)

class AuditContext:
    @staticmethod
    def get_source_type(request):
        if not request:
            return AuditLog.SourceOfEntry.SYSTEM
        
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        if not request.user.is_authenticated:
            if 'Postman' or 'Bruno' in user_agent:
                return AuditLog.SourceOfEntry.API_CLIENT_TOOL
            return AuditLog.SourceOfEntry.SYSTEM
        
        return AuditLog.SourceOfEntry.USER
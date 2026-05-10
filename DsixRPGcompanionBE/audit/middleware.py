# DsixRPGcompanionBE/audit/middleware.py
from threading import local
import json
from DsixRPGcompanionBE.models.audit_log import AuditLog

_audit_local = local()

class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        _audit_local.request = request
        response = self.get_response(request)
        return response
    
    @staticmethod
    def get_current_request():
        return getattr(_audit_local, 'request', None)

class AuditContext:
    @staticmethod
    def get_source_type(request):
        from DsixRPGcompanionBE.models.audit_log import AuditLog
        
        print(f"\n=== AuditContext.get_source_type called ===")
        print(f"request: {request}")
        print(f"request.user: {request.user}")
        print(f"request.user.is_authenticated: {request.user.is_authenticated}")
        print(f"request.META keys that might contain auth: {[k for k in request.META.keys() if 'AUTH' in k or 'HTTP_AUTHORIZATION' in k]}")
        
        if not request:
            print("No request - returning SYSTEM")
            return AuditLog.SourceOfEntry.SYSTEM
        
        print(f"request.user: {request.user}")
        print(f"request.user.is_authenticated: {request.user.is_authenticated}")
        
        if request.user.is_authenticated:
            print("User is authenticated - returning USER")
            return AuditLog.SourceOfEntry.USER
        
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        print(f"user_agent: {user_agent}")
        
        api_client_indicators = ['postman', 'bruno', 'insomnia', 'curl', 'httpie']
        if any(indicator in user_agent for indicator in api_client_indicators):
            print("API client detected - returning API_CLIENT_TOOL")
            return AuditLog.SourceOfEntry.API_CLIENT_TOOL
        
        print("Default fallback - returning SYSTEM")
        return AuditLog.SourceOfEntry.SYSTEM
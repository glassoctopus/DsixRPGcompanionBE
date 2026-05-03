# audit/decorators.py
from functools import wraps
from django.utils.decorators import method_decorator
from DsixRPGcompanionBE.audit.services import AuditService
from rest_framework.viewsets import ModelViewSet

def auto_audit(action):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            old_data = None
            original_instance = None
            
            # For UPDATE and DELETE, capture the current state from database BEFORE the action
            if action in ['UPDATE', 'DELETE'] and hasattr(self, 'get_object'):
                try:
                    original_instance = self.get_object()
                    if hasattr(self, 'get_serializer'):
                        serializer = self.get_serializer(original_instance)
                        old_data = serializer.data
                except Exception:
                    old_data = None
            
            # Execute the original view method
            response = view_func(self, request, *args, **kwargs)
            
            # For CREATE and UPDATE, capture the new state after the action
            if action in ['CREATE', 'UPDATE'] and hasattr(self, 'get_serializer'):
                try:
                    serializer = self.get_serializer()
                    if hasattr(serializer, 'instance'):
                        new_data = serializer.data if hasattr(serializer, 'data') else None
                        
                        AuditService.log(
                            action=action,
                            content_object=serializer.instance,
                            request=request,
                            old_data=old_data,
                            new_data=new_data
                        )
                except Exception:
                    pass
            elif action == 'DELETE' and original_instance:
                # For DELETE, log with the captured old_data (new_data is None)
                AuditService.log(
                    action=action,
                    content_object=original_instance,
                    request=request,
                    old_data=old_data,
                    new_data=None
                )
            
            return response
        return wrapper
    return decorator

# Usage in views
class EntryViewSet(ModelViewSet):
    @auto_audit('CREATE')
    def perform_create(self, serializer):
        serializer.save()
    
    @auto_audit('UPDATE')
    def perform_update(self, serializer):
        serializer.save()
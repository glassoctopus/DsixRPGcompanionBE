from django.contrib import admin
from DsixRPGcompanionBE.models.audit_log import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'get_source_type_display', 'get_action_display', 'user', 'object_id']
    list_filter = ['source_type', 'action', 'timestamp']
    search_fields = ['user__username', 'object_id']
    readonly_fields = ['id', 'source_type', 'action', 'user', 'timestamp', 'request_meta', 'old_data', 'new_data']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
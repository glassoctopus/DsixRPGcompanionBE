from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.conf import settings

class AuditLog(models.Model):
    class SourceOfEntry(models.TextChoices):
        USER = 'user', 'App User'
        SYSTEM = 'system', 'System Script / Auto loaded by App creator'
        API_CLIENT_TOOL = 'api_client_tool', 'Loaded by API client tool'
        SINGLE_IMPORT = 'single_import', 'Created as a single import entry'
        BULK_IMPORT = 'bulk_import', 'Created in a bulk import operation'
    
    class ActionType(models.TextChoices):
        CREATE = 'create', 'Create'
        UPDATE = 'update', 'Update'
        DELETE = 'delete', 'Delete'        
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    action = models.CharField(max_length=6, choices=ActionType.choices)
    source_type = models.CharField(max_length=15, choices=SourceOfEntry.choices)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    request_meta = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)
    old_data = models.JSONField(null=True, blank=True)
    new_data = models.JSONField(null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['timestamp']),
        ]
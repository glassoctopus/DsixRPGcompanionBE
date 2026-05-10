from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.conf import settings

class AuditLog(models.Model):
    class SourceOfEntry(models.TextChoices):
        USER = 'user', 'App User'
        SYSTEM = 'system', 'System Script / Auto loaded by App creator'
        API_CLIENT_TOOL = 'api_client_tool', 'Loaded by API client tool'
    
    class ActionType(models.TextChoices):
        CREATE = 'create', 'Create'
        UPDATE = 'update', 'Update'
        DELETE = 'delete', 'Delete'
    
    class SingleOrBulk(models.TextChoices):
        SINGLE_ENTRY_ACTION = 'single_entry_action', 'Created as a single entry transaction'
        BULK_ENTRIES_ACTION = 'bulk_entries_action', 'Created in a bulk entries transaction'
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    action = models.CharField(max_length=6, choices=ActionType.choices)
    source_type = models.CharField(max_length=16, choices=SourceOfEntry.choices)
    payload_type = models.CharField(max_length=19, choices=SingleOrBulk.choices)
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
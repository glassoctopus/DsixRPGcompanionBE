from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone   # you forgot this import

class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.CharField(max_length=113, null=True, blank=True)
    game_master = models.BooleanField(default=False)
    game_master_requested = models.BooleanField(default=False)
    game_master_approved = models.BooleanField(default=False)
    game_master_requested_at = models.DateTimeField(null=True, blank=True)
    
    game_master_request_to = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='received_requests',
        help_text="The admin/superuser this request was sent to"
    )
    game_master_approved_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_requests',
        help_text="The admin/superuser who approved this GM request"
    )
    
    def __str__(self):
        return self.username   # username exists from AbstractUser
    
    @property
    def is_game_master(self):
        """Check if user is an active Game Master"""
        return self.game_master and self.game_master_approved
    
    def request_game_master(self, admin_user=None):
        """Request GM status (called when user checks the box)"""
        self.game_master_requested = True
        self.game_master_request_to = admin_user
        self.game_master_requested_at = timezone.now()
        self.save()
    
    def approve_game_master(self, approver):
        """Approve GM request (called by admin)"""
        if approver.is_superuser or approver.is_staff:   # use is_staff, not custom 'admin'
            self.game_master = True
            self.game_master_approved = True
            self.game_master_approved_by = approver
            self.save()
            return True
        return False
    
    def reject_game_master(self):
        """Reject GM request"""
        self.game_master_requested = False
        self.game_master = False
        self.game_master_approved = False
        self.save()
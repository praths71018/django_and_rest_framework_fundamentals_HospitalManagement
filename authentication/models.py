from django.db import models
from django.contrib.auth.models import User

class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField()
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.user.username if self.user else 'Unknown User'} - {self.timestamp} - {'Success' if self.success else 'Failure'}"

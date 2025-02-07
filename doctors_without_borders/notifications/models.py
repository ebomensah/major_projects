from django.db import models
from users.models import CustomUser

class Notification(models.Model):
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField(blank=False)
    read_status = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.title} {self.recipient.first_name} {self.recipient.last_name} - {self.message[:30]}; Read: {self.read_status}"
    


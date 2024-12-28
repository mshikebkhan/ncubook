from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    NOTIFICATION_TYPES = ((1,'Like Post'),(2,'Add Comment'),(3,'Accepted Buddy Request'))

    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name="noti_post", blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_from_user", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_to_user")
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    preview = models.CharField(max_length=100, null=True, blank=True)
    is_seen = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

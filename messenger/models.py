from django.db import models
from django.contrib.auth.models import User

class DM(models.Model):
    "Direct Message"
    # Users
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dm_owner')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dm_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)

    # Main Content
    body = models.TextField(max_length=100)

    # Meta Info
    seen = models.BooleanField(default=False)

    # Date
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    # Make Sure That Save Function Runs Only 1 Time
    sent = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Direct Message"
        verbose_name_plural = "Direct Messages"

    def save(self, *args, **kwargs):
    	# Make A Copy For Receiver
        if not self.pk and self.sent == False:
            foo = DM(owner=self.receiver, sender=self.sender, receiver=self.receiver, body=self.body, sent=True)
            foo.save()	     
        super(DM, self).save(*args, **kwargs)

    def __str__(self):
        return self.body[:50]

from django.db import models

class Announcement(models.Model):
    body = models.CharField(max_length=150)
    def __str__(self):
        return str(self.body) 

    class Meta:
         verbose_name_plural = "Announcement"
from django.db import models
from django.conf import settings
import datetime

def event_image_upload_path(instance, filename):
    now = datetime.datetime.now()
    return (
        f"user_{instance.user.id}/"
        f"date_{now.year}_{now.month}_{now.day}/"
        f"time_{now.hour}_{now.minute}_{now.second}/"
        f"{filename}"
    )
class Event(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='events', on_delete=models.CASCADE)
    content=models.CharField(max_length=4000)
    event_image=models.ImageField(upload_to=event_image_upload_path,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    category=models.CharField(max_length=3000,default=None,blank=True,null=True)
    
    class Meta:
        db_table = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.content
    
class VoteEvent(models.Model):
    event = models.ForeignKey(Event, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("event", "user"), )
        db_table = 'VoteEvent'
        verbose_name_plural = 'VoteEvents'

    def __str__(self):
        return self.event.content

class EventComment(models.Model):
    event = models.ForeignKey(Event, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'EventComment'
        verbose_name_plural = 'EventComments'
        ordering = ['-created_at']

    def __str__(self):
        return self.comment
    

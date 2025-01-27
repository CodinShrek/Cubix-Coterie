from django.db import models
from django.utils.text import slugify
from user.models import Account
from datetime import datetime

# Create your models here.
from django.db.models.signals import pre_save
from django.db.models.signals import post_delete
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User
from autoslug import AutoSlugField 


def video_location(instance, filename, **kwargs):
    # Format the path for video upload, using the user's ID and the subject of the CommunityChat instance #
    video_path = 'community/{user_id}/{subject}-{filename}'.format(
        user_id=str(instance.user.id), # Convert user ID to string for path #
        subject =str(instance.subject), # Use the subject as part of the path #
        filename=filename # Filename is passed directly #
    )
    
    return video_path

class CommunityChat(models.Model):
    subject = models.CharField(max_length=100, blank=False, null=False)
    content = models.TextField(max_length=1000, null=False)
    
    # FileField for uploading video files, using the custom upload location defined in video_location #
    video = models.FileField( upload_to=video_location)
    video_details = models.DateTimeField(auto_now_add=True)
    
    # ForeignKey to link the chat to a user, deletes chat if the user is deleted #
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # AutoSlugField to automatically create a unique slug from the subject field #
    slug = AutoSlugField(populate_from='subject', unique=True)
    
    def __str__(self):
        return self.subject

# Signal to delete the associated video file from storage when a CommunityChat instance is deleted #
@receiver(post_delete, sender=CommunityChat)
def request_delete(sender,instance, **kwargs):
    instance.video.delete(False) # Set delete to False to avoid deleting the model instance #
    

        
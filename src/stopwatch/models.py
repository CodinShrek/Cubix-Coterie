from django.db import models
from django.contrib.auth.models import User # Import for foreign key reference #

from django.conf import settings

class StopwatchEntry(models.Model):
    # ForeignKey to associate each stopwatch entry with a user, delete entries if the user is deleted #
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=False, blank=False)
    duration = models.DurationField(null=False, blank=False)
    
    # Override the save method to calculate duration before saving the model instance #
    def save(self, *args, **kwargs):
        if self.end_time:
            # Calculate the duration as the difference between end_time and start_time #
            self.duration = self.end_time - self.start_time
        super(StopwatchEntry, self).save(*args, **kwargs)
        
        
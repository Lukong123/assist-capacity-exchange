import datetime

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class Bug(models.Model):
    description = models.CharField(max_length=200)
    bug_type = models.CharField(max_length=200)
    report_date = models.DateTimeField("report date")
    status = models.CharField(max_length=200)
    # description", "bug_type", "report_date", "status"

    def __str__(self):
        return self.bug_type
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.report_date <= now

    # def save(self, *args, **kwargs):
    #     self.full_clean()  
    #     super().save(*args, **kwargs)
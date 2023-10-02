from django.db import models

class Bug(models.Model):
    description = models.CharField(max_length=200)
    bug_type = models.CharField(max_length=200)
    report_date = models.DateTimeField("report date")
    status = models.CharField(max_length=200)
    # description", "bug_type", "report_date", "status"
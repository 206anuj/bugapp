from django.db import models

# Create your models here.


class Bug(models.Model):

    project = models.CharField(max_length=64)
    SDM = models.CharField(max_length=64)
    issue_reported = models.CharField(max_length=512)
    resolved_by = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project} || {self.SDM} || {self.issue_reported} || {self.resolved_by} || {self.created_at}"
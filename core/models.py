from django.db import models

class RequestLog(models.Model):
    kind = models.CharField(max_length=20)
    prompt_masked = models.TextField()
    response = models.TextField()
    pii_count = models.IntegerField(default=0)
    pii_types = models.JSONField(default=dict, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created"]

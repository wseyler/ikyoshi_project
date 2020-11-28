from django.db import models

class Style(models.Model):
    title = models.CharField(max_length=30, blank=False)
    originator = models.CharField(max_length=30, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

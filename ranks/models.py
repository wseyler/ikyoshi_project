from django.db import models
from styles.models import Style

class RankType(models.Model):
    style = models.ForeignKey('styles.Style', on_delete=models.CASCADE)
    ordinal = models.PositiveIntegerField(default=0, blank=False, null=False)
    title = models.CharField(max_length=100, blank=False)
    indicator = models.CharField(max_length=50, blank=True, null=True)
    time_in_grade = models.PositiveIntegerField(blank=True, null=True)
    time_in_style = models.PositiveIntegerField(blank=True, null=True)
    test_required = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    class Meta(object):
        ordering = ['ordinal']

    def __str__(self):
        return self.style.title + ", " + self.title

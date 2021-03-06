from django.db import models
from people.models import MartialArtist
from styles.models import Style

class TrainingClass(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    instructors = models.ManyToManyField(MartialArtist, related_name='class_instructors')
    students = models.ManyToManyField(MartialArtist)
    focus = models.ManyToManyField(Style)
    notes = models.TextField(blank=True, null=True)

    def duration_in_mins(self):
        tdelta = self.end - self.start
        return tdelta.total_seconds() / 60

    class Meta:
        # Add verbose name
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

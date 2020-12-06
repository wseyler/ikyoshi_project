from django.db import models
from people.models import MartialArtist
from styles.models import Style

class TrainingClass(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    instructor = models.ForeignKey(MartialArtist, related_name="class_instructor", on_delete=models.SET_NULL, blank=True, null=True )
    students = models.ManyToManyField(MartialArtist)
    focus = models.ManyToManyField(Style)
    notes = models.TextField(blank=True, null=True)

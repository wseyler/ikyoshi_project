from django.contrib import admin
from .models import TrainingClass

@admin.register(TrainingClass)
class TrainingClassAdmin(admin.ModelAdmin):
    list_display = ['start', 'end', 'duration_in_mins', 'notes']
    list_display_links = ['start', 'end', 'duration_in_mins']
    list_filter=['start']
    ordering = ('-start',)
    fieldsets = (
        ('Class Info', {
            'fields' : ('start', 'end', 'focus', 'notes')
        }),
        ('Attendence', {
            'fields' : ('instructors', 'students')
        })
    )

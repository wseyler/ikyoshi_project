from django.contrib import admin
from .models import TrainingClass

class TrainingClassAdmin(admin.ModelAdmin):
    list_display = ['start', 'end', 'duration_in_mins', 'instructor', 'notes']
    list_filter = ['instructor']
    fieldsets = (
        ('Class Info', {
            'fields' : ('start', 'end', 'focus', 'notes')
        }),
        ('Attendence', {
            'fields' : ('instructor', 'students')
        })
    )

admin.site.register(TrainingClass, TrainingClassAdmin)

from django.contrib import admin
from .models import TrainingClass

class TrainingClassAdmin(admin.ModelAdmin):
    list_display = ['start', 'end', 'duration_in_mins', 'instructor', 'notes']
    list_filter = ['instructor']

admin.site.register(TrainingClass, TrainingClassAdmin)

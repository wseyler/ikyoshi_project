from django.contrib import admin
from .models import TrainingClass

class TrainingClassAdmin(admin.ModelAdmin):
    list_display = ['start', 'end', 'instructor', 'notes']

admin.site.register(TrainingClass, TrainingClassAdmin)

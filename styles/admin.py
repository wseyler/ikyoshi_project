from django.contrib import admin

from .models import Style
from ranks.models import RankType

class RankTypeInline(admin.TabularInline):
    model = RankType
    extra = 1
    exclude = ('ordinal',)

@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ['title', 'originator', 'notes']
    inlines = [RankTypeInline]

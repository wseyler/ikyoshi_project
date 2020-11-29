from django.contrib import admin

from .models import Style
from ranks.models import RankType

class RankTypeInline(admin.TabularInline):
    model = RankType
    extra = 3
    exclude = ('ordinal',)

class StyleAdmin(admin.ModelAdmin):
    inlines = [RankTypeInline]

admin.site.register(Style, StyleAdmin)

from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import RankType

@admin.register(RankType)
class RankTypeAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass

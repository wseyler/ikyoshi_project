from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import RankType
from .models import Rank

@admin.register(RankType)
class RankTypeAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass

admin.site.register(Rank)

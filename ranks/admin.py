from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import RankType
from .models import Rank

class RankTypeAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['ordinal', 'style', 'title', 'indicator', 'time_in_grade', 'time_in_style', 'test_required']

    def place(self, obj):
        return obj.ordinal

class RankAdmin(admin.ModelAdmin):
    list_display = ['martial_artist', 'rank_type', 'test_date', 'award_date', 'tested']

admin.site.register(RankType, RankTypeAdmin)
admin.site.register(Rank, RankAdmin)

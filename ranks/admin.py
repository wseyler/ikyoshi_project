from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import RankType
from .models import Rank

@admin.register(RankType)
class RankTypeAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['ordinal', 'style', 'title', 'indicator', 'time_in_grade', 'time_in_style', 'test_required']
    list_filter = ['test_required', 'style__title', 'indicator']
    list_display_links = ['style', 'title', 'indicator']
    fieldsets = (
        ('Type Info', {
            'fields' : ('style', 'title', 'indicator')
        }),
        ('Testing Info', {
            'fields' : ('time_in_grade', 'time_in_style', 'test_required', 'notes')
        })
    )

    def place(self, obj):
        return obj.ordinal

@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ['martial_artist', 'rank_type', 'test_date', 'award_date', 'tested']
    list_filter = ['martial_artist', 'award_date', 'tested']
    list_display_links = ['martial_artist', 'rank_type']
    search_fields = ['rank_type__title', 'rank_type__style__title']

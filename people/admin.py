from django.contrib import admin
from django.utils.html import format_html

from .models import MartialArtist, Sponsor
from ranks.models import Rank

class RankInline(admin.StackedInline):
    model = Rank
    extra = 1

class MartialArtistAdmin(admin.ModelAdmin):
    model = MartialArtist
    inlines = [RankInline]
    list_display = ['last_name', 'first_name', 'enrollment_date', 'sponsor', 'image_tag']

    def image_tag(self,obj):
        if obj.image:
            return format_html('<img src="{0}" style="width: 45px; height:45px;" />'.format(obj.image.url))
        else:
            return ""

class SponsorAdmin(admin.ModelAdmin):
    model = Sponsor
    list_display = ['first_name', 'middle_name', 'last_name', 'email', 'street', 'city', 'state', 'zip', 'telephone', 'isParent']

admin.site.register(MartialArtist, MartialArtistAdmin)
admin.site.register(Sponsor, SponsorAdmin)

from django.contrib import admin
from django.utils.html import format_html

from .models import MartialArtist, Sponsor
from ranks.models import Rank
from tuition.models import TuitionPayment

class RankInline(admin.TabularInline):
    model = Rank
    extra = 1
    ordering = ('-award_date',)

class TuitionPaymentInLine(admin.TabularInline):
    model = TuitionPayment
    extra = 1
    ordering = ('-date_paid',)


@admin.register(MartialArtist)
class MartialArtistAdmin(admin.ModelAdmin):
    model = MartialArtist
    inlines = [TuitionPaymentInLine, RankInline]
    list_display = ['last_name', 'first_name', 'enrollment_date', 'sponsor', 'active', 'image_tag_small']
    list_filter = ['active', 'sponsor']
    list_display_links = ['last_name', 'first_name']
    search_fields = ['last_name', 'first_name']
    readonly_fields = ['martial_artist_image']
    fieldsets = (
        ('Personal Info', {
            'fields' : ('first_name', 'middle_name', 'last_name', 'email', 'sponsor', 'birthday', 'isFemale', 'image', 'martial_artist_image', 'notes')
        }),
        ('Dojo Info', {
            'fields' : ('enrollment_date', 'payment_plan', 'active')
        })
    )

    def martial_artist_image(self, obj):
        if obj.image:
            return format_html('<img src="{0}" style="width: 180px; height:180px;" />'.format(obj.image.url))
        else:
            return ""

    def image_tag_small(self, obj):
        if obj.image:
            return format_html('<img src="{0}" style="width: 45px; height:45px;" />'.format(obj.image.url))
        else:
            return ""

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    model = Sponsor
    list_display = ['first_name', 'middle_name', 'last_name', 'email', 'street', 'city', 'state', 'zip', 'telephone', 'isParent']
    search_fields = ['last_name', 'first_name']
    fieldsets = (
        ('Personal Info', {
            'fields' : ('first_name', 'middle_name', 'last_name', 'isParent')
        }),
        ('Contact Info', {
            'fields' : ('street', 'city', 'state', 'zip', 'telephone')
        })
    )

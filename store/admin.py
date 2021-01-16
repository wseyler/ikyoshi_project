from django.contrib import admin
from .models import Item, Invoice, LineItem

class LineItemInline(admin.TabularInline):
    model = LineItem
    extra = 0



@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    model = Invoice
    inlines = [LineItemInline]
    list_display = ['id', 'purchaser', 'date_ordered', 'date_completed', 'invoice_total', 'is_completed']
    list_display_links = ['id', 'purchaser', 'date_ordered', 'date_completed', 'invoice_total']
    def is_completed(self, obj):
        return obj.date_completed != None

admin.site.register(Item)

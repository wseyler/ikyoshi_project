from django.contrib import admin
from .models import Item, Invoice, LineItem

class LineItemInline(admin.TabularInline):
    model = LineItem
    extra = 0

class InvoiceAdmin(admin.ModelAdmin):
    model = Invoice
    inlines = [LineItemInline]
    list_display = ["id", "purchaser", "date_ordered", "date_completed", "invoice_total"]

admin.site.register(Item)
admin.site.register(Invoice, InvoiceAdmin)
# admin.site.register(LineItem)
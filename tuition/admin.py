from django.contrib import admin
from .models import PaymentPlan, TuitionPayment

class TuitionPaymentInline(admin.TabularInline):
    model = TuitionPayment
    extra = 1
    ordering = ("-date_paid",)

class PaymentPlanAdmin(admin.ModelAdmin):
    model = PaymentPlan
    inlines = [TuitionPaymentInline]

class TuitionPaymentAdmin(admin.ModelAdmin):
    model = TuitionPayment
    list_display = ['date_paid', 'payer', 'paid', 'payment_plan']
    list_filter = ['payer', 'payment_plan']
    list_display_links = ['date_paid', 'payer', 'paid']

admin.site.register(PaymentPlan, PaymentPlanAdmin)
admin.site.register(TuitionPayment, TuitionPaymentAdmin)

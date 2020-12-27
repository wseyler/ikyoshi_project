from django.contrib import admin
from .models import PaymentPlan, TuitionPayment

class TuitionPaymentInline(admin.TabularInline):
    model = TuitionPayment
    extra = 1
    ordering = ("-date_paid",)

@admin.register(PaymentPlan)
class PaymentPlanAdmin(admin.ModelAdmin):
    model = PaymentPlan
    inlines = [TuitionPaymentInline]

@admin.register(TuitionPayment)
class TuitionPaymentAdmin(admin.ModelAdmin):
    model = TuitionPayment
    list_display = ['date_paid', 'payer', 'paid', 'payment_plan']
    list_filter = ['payer', 'payment_plan']
    list_display_links = ['date_paid', 'payer', 'paid']

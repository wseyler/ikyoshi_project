from django.db import models
from datetime import datetime

class PaymentPlan(models.Model):
    NONE_FREQUENCY = 0
    MONTHLY_FREQUENCY = 1
    BI_MONTHLY_FREQUENCY = 2
    QUARTERLY_FREQUENCY = 3
    SEMI_ANNUAL_FREQENCY = 6
    ANNUAL_FREQUENCY = 12
    FREQUENCY_CHOICES = (
        (NONE_FREQUENCY, 'None'),
        (MONTHLY_FREQUENCY, 'Monthly'),
        (BI_MONTHLY_FREQUENCY, "Bi-Monthly"),
        (QUARTERLY_FREQUENCY, 'Quarterly'),
        (SEMI_ANNUAL_FREQENCY, 'Semi-annual'),
        (ANNUAL_FREQUENCY, 'Annual'),
    )

    title = models.CharField(max_length=30, blank=False)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    frequency = models.IntegerField(choices=FREQUENCY_CHOICES, default=MONTHLY_FREQUENCY)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class TuitionPayment(models.Model):
    payment_plan = models.ForeignKey(PaymentPlan, on_delete=models.SET_NULL, blank=True, null=True )
    payer = models.ForeignKey("people.MartialArtist", on_delete=models.CASCADE)
    date_paid = models.DateField()
    paid = models.DecimalField(max_digits=6, decimal_places=2)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.date_paid.strftime("%m/%d/%Y") + ' - ' + str(self.payer) + ' - $' + str(self.paid)

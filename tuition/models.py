from django.db import models

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

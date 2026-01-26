from django.db import models
from people.models import MartialArtist

class Item(models.Model):
    name = models.CharField(max_length=50)
    make = models.CharField(max_length=50, blank=True, null=True)
    sku = models.CharField(max_length=30, blank=True, null=True)
    size = models.CharField(max_length=10, blank=True, null=True)
    color = models.CharField(max_length=10, blank=True, null=True)
    wholesale_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    retail_price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity_on_hand = models.SmallIntegerField(default=0)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    purchaser = models.ForeignKey('people.MartialArtist', on_delete=models.CASCADE)
    date_ordered = models.DateField(auto_now_add=True)
    date_completed = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['-date_ordered']),
            models.Index(fields=['purchaser', '-date_ordered']),
        ]
        ordering = ['-date_ordered']

    def __str__(self):
        return f'Invoice #{self.id}'

    def invoice_total(self):
        """Optimized invoice total calculation using database aggregation"""
        from django.db.models import Sum, F
        total = self.lineitem_set.aggregate(
            total=Sum(F('item__retail_price') * F('quantity'))
        )['total']
        return total or 0


class LineItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

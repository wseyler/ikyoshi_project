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

    def __str__(self):
        return str(self.id)

    def invoice_total(self):
        total = 0
        for li in self.lineitem_set.all():
            total += li.item.retail_price * li.quantity
        return total


class LineItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

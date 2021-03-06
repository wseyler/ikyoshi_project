from django.db import models
from styles.models import Style
from tuition.models import PaymentPlan

class Person(models.Model):
    first_name = models.CharField(max_length=30, blank=False)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        name = self.first_name
        if self.middle_name != None and len(self.middle_name) > 0:
            name = name + ' ' + self.middle_name[0] + '.'
        name = name + ' ' + self.last_name
        return name

    class Meta:
        abstract = True
        ordering = ['last_name', 'first_name']

class Sponsor(Person):
    isParent = models.BooleanField(default=True)
    street = models.CharField(max_length=70, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)

class MartialArtist(Person):
    isFemale = models.BooleanField(default=False)
    styles = models.ManyToManyField(Style)
    enrollment_date = models.DateField(blank=True, null=True)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.SET_NULL, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='people/images', blank=True, null=True)
    active = models.BooleanField(default=True)
    payment_plan = models.ForeignKey(PaymentPlan, on_delete=models.SET_NULL, blank=True, null=True)

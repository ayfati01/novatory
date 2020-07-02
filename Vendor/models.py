from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class Vendor(models.Model):
    Name    = models.CharField(max_length=100, blank=False)
    Balance = models.DecimalField(decimal_places=2, blank=True, max_digits=7)
    ContactName     = models.CharField(max_length=100, blank=True)
    ContactPhone    = PhoneNumberField(blank=True)
    ContactFax      = PhoneNumberField(blank=True)
    ContactEmail    = models.EmailField(blank=True)
    ContactWebsite  = models.CharField(max_length=200, blank=True)
    PurchasingPayDuration = models.IntegerField(help_text='Duration in days to pay balance', blank=True)
    PurchasingDiscount    = models.DecimalField(decimal_places=1, max_digits=5)
    PurchasingTaxRate     = models.DecimalField(default=6.0, max_digits=7, decimal_places=2, validators=[MaxValueValidator(7), MinValueValidator(4)])

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name_plural = 'Vendors'
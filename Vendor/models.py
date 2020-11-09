from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator
from gtin_fields.fields import UPCAField
from taggit.managers import TaggableManager
import math
import locale


def pretty_print_currency(amt):
    locale.setlocale(
        locale.LC_ALL,
        'en_US.UTF-8')

    return locale.currency(amt, grouping=True)


# Create your models here.


class Vendor(models.Model):
    Name    = models.CharField(max_length=100, blank=False)
    Balance = models.DecimalField(decimal_places=2, blank=True, max_digits=8)
    Contact_name     = models.CharField(max_length=100, blank=True)
    Contact_phone    = PhoneNumberField(blank=True)
    Contact_fax      = PhoneNumberField(blank=True)
    Contact_email    = models.EmailField(blank=True)
    Contact_website  = models.CharField(max_length=200, blank=True)
    Purchasing_pay_duration = models.IntegerField(help_text='Duration in days to pay balance', blank=True)
    Purchasing_discount     = models.DecimalField(decimal_places=1, max_digits=5)
    Purchasing_tax_rate     = models.DecimalField(default=6.0, max_digits=7, decimal_places=2, validators=[MaxValueValidator(7), MinValueValidator(4)])

    def __str__(self):
        # to display the balance nicely, we'll use the locale library
        # by setting the region to US and then use the currency feature
        return f"Vendor: {self.Name} | Balance: {pretty_print_currency(self.Balance)}"

    class Meta:
        verbose_name_plural = 'Vendors'


class Item(models.Model):
    Name = models.CharField(max_length=16, blank=False, unique=True)
    Expire = models.DateField(help_text="Expiration date for product. If product doesn't have an expiration date, leave blank", blank=True)
    UPC = UPCAField()
    ITEM_STATUS_CHOICES = [
        (1, 'Item is on shelf'),
        (0, 'Item is not on shelf')
    ]
    Amount_in_stock = models.IntegerField(help_text="Amount in stock", name="# of items in stock", blank=False)
    is_on_shelf = models.CharField(max_length=2, choices=ITEM_STATUS_CHOICES, default=0)
    Amount_on_shelf = models.IntegerField(help_text="Amount on shelf", name="# of items on shelf. If item is not on shelf, leave blank.", blank=True)
    Tags = TaggableManager()

    def pretty_name(self):
        chars = 16-len(self.Name)
        borders = str("#"*(math.floor(chars/2)))
        template = borders+self.Name.upper()+borders
        return template

    def __str__(self):
        return f"{self.pretty_name()} UPC:{self.UPC}"


class Payment(models.Model):
    Vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    Amount = models.DecimalField(decimal_places=2, blank=True, max_digits=8)
    Payment_date = models.DateField(name="Payment date", help_text="Day of payment")
    Check_number = models.IntegerField(help_text="If payment wasn't made with check, leave blank", blank=True)

    def __str__(self):
        return f"Vendor: {self.Vendor.Name} | Amount: {pretty_print_currency(self.Amount)} | Check number: {str(self.Check_number)}"


class Invoice(models.Model):
    Vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    Number = models.BigIntegerField(name="Invoice number", blank=True)
    Order_date = models.DateField(help_text="Date when the goods where ordered.")
    Delivery_date = models.DateField(help_text="Date when the goods where delivered.")
    Payments = models.ManyToManyField(Payment)
    Items = models.ManyToManyField(Item)

    def __str__(self):
        return f"Vendor: {self.Vendor} Delivered on {self.delivery_date}"

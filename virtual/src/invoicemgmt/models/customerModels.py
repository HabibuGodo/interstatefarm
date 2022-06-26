from datetime import datetime
from django.db import models
from django.db.models.deletion import CASCADE
from django.conf import settings
from django.contrib.auth.models import User
from PIL import Image
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
datetime.strptime('2014-12-04', '%Y-%m-%d').date()

# Create your models here.


class Orders(models.Model):
    customer = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=CASCADE, null=True)
    order_date = models.DateField(
        auto_now_add=False, auto_now=True, blank=True, null=True)
    order_completion_date = models.DateField(
        auto_now_add=False, auto_now=False, blank=True, null=True)
    gram_90_beans = models.IntegerField(default=0, blank=True, null=True)
    gram_90_ground = models.IntegerField(default=0, blank=True, null=True)
    gram_250_beans = models.IntegerField(default=0, blank=True, null=True)
    gram_250_ground = models.IntegerField(default=0, blank=True, null=True)
    gram_400_beans = models.IntegerField(default=0, blank=True, null=True)
    gram_400_ground = models.IntegerField(default=0, blank=True, null=True)
    gram_750_beans = models.IntegerField(default=0, blank=True, null=True)
    gram_750_ground = models.IntegerField(default=0, blank=True, null=True)
    kilogram_1_beans = models.IntegerField(default=0, blank=True, null=True)
    kilogram_1_ground = models.IntegerField(default=0, blank=True, null=True)
    total_kg_beans = models.DecimalField(
        default=0, max_digits=5, blank=True, null=True, decimal_places=2,)
    total_kg_ground = models.DecimalField(
        default=0, max_digits=5, blank=True, null=True, decimal_places=2,)
    total_kgs = models.DecimalField(
        'Total Kg', default=0, max_digits=9, decimal_places=2, null=True)
    amount_tzs = models.DecimalField(
        'Total Amount(TZS)', default=0, max_digits=9, blank=True, decimal_places=2, null=True)
    amount_usd = models.DecimalField(
        'Total Amount(USD)', default=0, max_digits=9, blank=True, decimal_places=2, null=True)
    amount_vat_tzs = models.DecimalField(
        'Total VAT 18%(TZS)', default=0, max_digits=9, blank=True, decimal_places=2, null=True)
    amount_vat_usd = models.DecimalField(
        'Total VAT 18%(USD)', default=0, max_digits=9, blank=True, decimal_places=2, null=True)
    amount_sub_total_tzs = models.DecimalField(
        'Sub-Total Amount(TZS)', default=0, max_digits=9, blank=True, decimal_places=2, null=True)
    amount_sub_total_usd = models.DecimalField(
        'Sub-Total Amount(USD)', default=0, max_digits=9, blank=True, decimal_places=2, null=True)
    
    STATUS = (
        ('New', 'New'),
        ('Invoice Generated', 'Invoice Generated'),
        ('Paid Some', 'Paid Some'),
        ('Paid', 'Paid'),
    )
    order_status = models.CharField(
        'Status', max_length=20, default='New', blank=True, choices=STATUS, null=True)
    payment_status = models.CharField(
        'Payment Status', max_length=20, default='Not Paid', blank=True, null=True)
        
    updated_by = models.CharField(
        'Updated By', max_length=20, default='', blank=True, null=True)


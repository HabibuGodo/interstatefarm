from datetime import datetime
from django.db import models
from django.db.models.deletion import CASCADE
from django.conf import settings
from django.contrib.auth.models import User
from PIL import Image
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
datetime.strptime('2014-12-04', '%Y-%m-%d').date()

# Create your models here.


class CompanyInfo(models.Model):
    # company info
    company_name = models.CharField(
        'Company Name', max_length=120, default='', blank=True, null=True)
    post_address = models.CharField(
        'P.O. Box', max_length=10, default='', blank=True, null=True)
    phone_number = models.CharField(
        'Phone Number', max_length=16, default='', blank=True, null=True)
    phone_number2 = models.CharField(
        'Phone Number 2', max_length=16, default='', blank=True, null=True)
    email_address = models.CharField(
        'Email', max_length=150, default='', blank=True, null=True)
    region = models.CharField('Region', max_length=50,
                              default='', blank=True, null=True)
    vision = models.CharField('Vision', max_length=50,
                              default='', blank=True, null=True)
    mission = models.CharField('Mission', max_length=50,
                               default='', blank=True, null=True)
    about = models.TextField('About Organization', max_length=5000,
                             default='', blank=True, null=True)
    country = models.CharField(
        'Country', max_length=150, default='', blank=True, null=True)
    vrn_number = models.CharField(
        'VRN', max_length=15, default='', blank=True, null=True)
    tin_number = models.CharField(
        'TIN', max_length=15, default='', blank=True, null=True)
    company_website = models.CharField(
        'Website', max_length=150, default='', blank=True, null=True)
    facebook = models.CharField(
        'Facebook', max_length=150, default='', blank=True, null=True)
    twitter = models.CharField(
        'Twitter', max_length=150, default='', blank=True, null=True)
    instagram = models.CharField(
        'Instagram', max_length=150, default='', blank=True, null=True)
    hours = models.CharField(
        'Hours', max_length=150, default='', blank=True, null=True)
    location = models.TextField(
        'Location', max_length=500, default='', blank=True, null=True)
    bank_tzs = models.CharField(
        'TZS', max_length=30, default='', blank=True, null=True)
    bank_usd = models.CharField(
        'USD', max_length=150, default='', blank=True, null=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Invoice(models.Model):

    invoice_number = models.IntegerField(blank=True, null=False)
    invoice_date = models.DateField(
        auto_now_add=True, auto_now=False, blank=True, null=True)

    # customer info
    customer_name = models.CharField(
        'customer Name', max_length=120, default='', blank=True, null=True)
    post_address = models.CharField(
        'P.O. Box', max_length=10, default='', blank=True, null=True)
    phone_number = models.CharField(
        max_length=15, default='', blank=True, null=True)
    email_address = models.CharField(
        'Email', max_length=150, default='', blank=True, null=True)

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
        default=0, max_digits=5, blank=True, null=True, decimal_places=2)
    total_kgs = models.DecimalField(
        'Total Kg', default=0, max_digits=9, decimal_places=2, null=True)

    # Invoice total
    sub_total = models.IntegerField(default=0, blank=True, null=True)
    tax = models.IntegerField(default=0, blank=True, null=True)
    discount = models.IntegerField(default=0, blank=True, null=True)
    discount_rate = models.IntegerField(default=0, blank=True, null=True)
    total = models.IntegerField(default=0, blank=True, null=True)
    document_type = models.CharField(
        max_length=50, default='', blank=True, null=True)
    payment_status = models.CharField(
        'Payment Status', max_length=20, default='Not Paid', blank=True, null=True)
    def __str__(self):
        return str(self.invoice_number)


class Stock(models.Model):
    package_type = models.CharField(
        'Package Type', max_length=50, default='', blank=True, null=False)
    new_stock = models.IntegerField(
        'New Stock', default=0, blank=True, null=True)
    previous_stock = models.IntegerField(
        'Previous Added', default=0, blank=True, null=True)
    new_stock_date = models.DateField(auto_now_add=True, auto_now=False)
    previous_stock_date = models.DateField(
        auto_now_add=False, auto_now=False, blank=True, null=True)
    total = models.IntegerField('Total Pcs', default=0, blank=True, null=True)
    total_kg = models.DecimalField(
        'Total Kilograms', default=0, blank=True, null=True, max_digits=12, decimal_places=2)
    wholesale_total_price = models.IntegerField(
        'Wholesale Total Price', default=0, blank=True, null=True)
    retail_total_price = models.IntegerField(
        'Retail Total Price', default=0, blank=True, null=True)


class Customer(models.Model):
    customer_name = models.CharField(
        'Customer Name', max_length=100, default='', blank=True, null=True)
    postal_address = models.CharField(
        'Postal Address', max_length=200, default='', blank=True, null=True)
    email = models.EmailField(
        'Email Address', max_length=150, default='', blank=True, null=True,)
    phone_number = models.CharField(
        'Phone Number', max_length=150, default='', blank=True, null=True)
    visible = models.IntegerField(default='0',null=True)
    user = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    added_by = models.CharField(
        'Added By', max_length=150, default='', blank=True, null=True)

    def __str__(self):
        return self.customer_name


class PackageList(models.Model):
    package_name = models.CharField(
        'Package Name', max_length=50, default='', blank=True, null=True)
    package_weight = models.DecimalField(
        'Package Weight', blank=True, null=True, max_digits=5, decimal_places=2)
    wholesale_price = models.IntegerField(
        'Whole Sale Price', blank=True, null=True)
    retail_price = models.IntegerField('Retail Price', blank=True, null=True)

    def __str__(self):
        return self.package_name


class Madeni(models.Model):
    customer = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    deni_amount_tzs = models.DecimalField(
        'Total Amount(TZS)', default=0, max_digits=9, blank=True, decimal_places=2, null=True)
    deni_amount_usd = models.DecimalField(
        'Total Amount(USD)', default=0, max_digits=9, blank=True, decimal_places=2, null=True)
    deni_due_date = models.DateField('Due Date',
                                     auto_now_add=False, auto_now=False, blank=True, null=True)
    created_at = models.DateField(
        auto_now_add=True, auto_now=False)
    served_by = models.CharField(
        'Updated By', max_length=20, default='', blank=True, null=True)

    def __str__(self):
        return self.customer


class Payments(models.Model):
    customer = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_number = models.CharField(
        'Order No', max_length=20, default='', blank=True, null=True)
    payment_date = models.DateField(
        auto_now_add=True, auto_now=False)
    paid_amount_tzs = models.DecimalField(
        'Total Amount(TZS)', default=0, max_digits=9, blank=True, decimal_places=2, null=True)
    paid_amount_usd = models.DecimalField(
        'Total Amount(USD)', default=0, max_digits=9, blank=True, decimal_places=2, null=True)
    proof_of_payment = models.FileField(
        default='default.png', upload_to='Proofs')
    updated_by = models.CharField(
        'Updated By', max_length=20, default='', blank=True, null=True)

    def __str__(self):
        return str(self.customer)

class Expenses(models.Model):
    payee = models.CharField(
        'Mlipwaji', max_length=100, default='', blank=True, null=True)
    description = models.TextField(
        'Maelezo ya malipo', max_length=250, default='', blank=True, null=True)
    payment_date = models.DateField(auto_now_add=True, auto_now=False)
    paid_amount = models.DecimalField(
        'Kiasi cha malipo', default=0, max_digits=9, blank=True, decimal_places=2, null=True)
    proof_of_payment = models.FileField(
        default='default.png', upload_to='Proofs_expenses')
    updated_by = models.CharField(
        'Paid By', max_length=20, default='', blank=True, null=True)
    def __str__(self):
        return str(self.payee)

# class Order(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     order_date = models.DateField(
#         auto_now_add=False, auto_now=False, blank=True, null=True)
#     order_completion_date = models.DateField(blank=True, null=True)
#     gram_90_beans = models.IntegerField(default=0, blank=True, null=True)
#     gram_90_ground = models.IntegerField(default=0, blank=True, null=True)
#     gram_250_beans = models.IntegerField(default=0, blank=True, null=True)
#     gram_250_ground = models.IntegerField(default=0, blank=True, null=True)
#     gram_400_beans = models.IntegerField(default=0, blank=True, null=True)
#     gram_400_ground = models.IntegerField(default=0, blank=True, null=True)
#     gram_750_beans = models.IntegerField(default=0, blank=True, null=True)
#     gram_750_ground = models.IntegerField(default=0, blank=True, null=True)
#     kilogram_1_beans = models.IntegerField(default=0, blank=True, null=True)
#     kilogram_1_ground = models.IntegerField(default=0, blank=True, null=True)
#     total_kg = models.DecimalField('Total Kg', max_digits=5, decimal_places=2)
#     amount = models.IntegerField('Total Amount')
#     GEEKS_CHOICES = (
#         ("New", "New"),
#         ("Pending", "Pending"),
#         ("Complete", "Complete")
#     )
#     order_status = models.CharField(
#         'Status', max_length=20, default='', choices=GEEKS_CHOICES, blank=True, null=True)
#     served_by = models.ForeignKey(
#         AUTH_USER_MODEL, on_delete=CASCADE, null=True)

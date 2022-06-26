from django.contrib import admin
from .models import *
from .forms import *

# Register your models here.


class companyInfoAdm(admin.ModelAdmin):
    list_display = ['tin_number', 'vrn_number', 'company_name',
                    'email_address', 'phone_number', 'post_address', 'region', 'country', 'company_website',
                    'bank_tzs', 'bank_usd']


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'customer_name', 'invoice_date', 'total']
    # form = InvoiceForm
    list_filter = ['customer_name']
    search_fields = ['customer_name',
                     'invoice_number', 'invoice_date', 'total']


class PackageAdmin(admin.ModelAdmin):
    list_display = ['package_name', 'package_weight',
                    'wholesale_price', 'retail_price']
    # form = InvoiceForm
    # list_filter = ['customer_name']
    # search_fields = ['customer_name','invoice_number','invoice_date','total']


class StockAdmin(admin.ModelAdmin):
    list_display = ['package_type', 'new_stock', 'previous_stock',
                    'new_stock_date', 'previous_stock_date', 'total']
    # form = InvoiceForm
    # list_filter = ['customer_name']
    # search_fields = ['customer_name','invoice_number','invoice_date','total']


class MadeniAdmin(admin.ModelAdmin):
    list_display = ['customer', 'deni_amount_tzs', 'deni_amount_usd', 'deni_due_date','served_by','created_at']
    list_filter = ['customer']
    search_fields = ['customer']

class PaymentsAdmin(admin.ModelAdmin):
    list_display = ['customer', 'paid_amount_tzs', 'paid_amount_usd', 'payment_date','updated_by','proof_of_payment']
    list_filter = ['payment_date','customer']
    search_fields = ['payment_date','customer']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'postal_address', 'email', 'phone_number']
    list_filter = ['customer_name']
    search_fields = ['customer_name']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'order_date', 'total_kgs', 'amount_tzs',
                    'order_status', 'order_completion_date', 'updated_by']
    list_filter = ['order_completion_date', 'order_date','customer', 'total_kgs',
                   'order_status']
    search_fields = ['customer', 'order_date', 'total_kgs', 'amount_tzs',
                     'order_status', 'order_completed_date', 'updated_by']

class KikundiAdmin(admin.ModelAdmin):
    list_display = ['namba_yakikundi', 'jina_laKikundi']

class FarmersAdmin(admin.ModelAdmin):
    list_display = ['jina', 'kijiji','kitongoji','ukubwa_washamba','namba_yasimu']


class ViongoziWaKikundiAdmin(admin.ModelAdmin):
    list_display = ['namba_yakikundi', 'jina', 'namba_yaNida',
                    'cheo', 'simu', 'jina2', 'namba_yaNida2',
                    'cheo2', 'simu2', 'jina3',
                    'namba_yaNida3', 'cheo3', 'simu3', 'jina4',
                    'namba_yaNida4', 'cheo4', 'simu4',]

admin.site.register(Home_contents)
admin.site.register(Home_slides)
admin.site.register(Partners)
admin.site.register(Teams)
admin.site.register(Expenses)
admin.site.register(AboutUs)
admin.site.register(Payments,PaymentsAdmin)
admin.site.register(Madeni,MadeniAdmin)
admin.site.register(Farmers,FarmersAdmin)
admin.site.register(Services)
admin.site.register(Careers)
admin.site.register(CareerExperience)
admin.site.register(CareerDuties)
admin.site.register(CompanyInfo, companyInfoAdm)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Profile)
admin.site.register(Stock, StockAdmin)
admin.site.register(Orders, OrderAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(PackageList, PackageAdmin)
admin.site.register(Kikundi, KikundiAdmin)
admin.site.register(ViongoziWaKikundi, ViongoziWaKikundiAdmin)

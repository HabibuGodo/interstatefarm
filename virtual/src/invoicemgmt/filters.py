from django.db.models import fields
import django_filters
from .models import *



class OrderFilters(django_filters.FilterSet):
    class Meta:
        model = Orders
        fields = ['order_date','customer','order_status'] 

class PaymentsFilters(django_filters.FilterSet):
    class Meta:
        model = Payments
        fields = ['customer','payment_date'] 

class MadeniFilters(django_filters.FilterSet):
    class Meta:
        model = Madeni
        fields = ['customer'] 
        # fields = ['customer','deni_due_date','served_by','created_at'] 

class CustomersFilters(django_filters.FilterSet):
    class Meta:
        model = Customer
        # fields = ['customer'] 
        fields = ['customer_name'] 

class WakulimaFilters(django_filters.FilterSet):
    class Meta:
        model = Farmers
        # fields = ['customer'] 
        fields = ['kijiji','kitongoji'] 
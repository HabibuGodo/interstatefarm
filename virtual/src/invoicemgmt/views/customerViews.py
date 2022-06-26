from typing import Counter
from django.contrib import auth
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.views.generic import View
from random import randrange
from ..forms import *
from ..models import *
from ..filters import *
# import datetime
from datetime import datetime


@login_required
def customer_home(request):

    company_info = CompanyInfo.objects.get()
    context = {
        'buttonTitle': 'Create',
        'company_info': company_info,
    }
    return render(request, 'customer/home.html', context)


@login_required
def orderNow(request):
    company_info = CompanyInfo.objects.get()
    form = OrderNowForm(request.POST or None)
    if form.is_valid():
        customer = request.user.id
        order_date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        gram_90_beans = form.cleaned_data['gram_90_beans']
        gram_90_ground = form.cleaned_data['gram_90_ground']
        gram_250_beans = form.cleaned_data['gram_250_beans']
        gram_250_ground = form.cleaned_data['gram_250_ground']
        gram_400_beans = form.cleaned_data['gram_400_beans']
        gram_400_ground = form.cleaned_data['gram_400_ground']
        gram_750_beans = form.cleaned_data['gram_750_beans']
        gram_750_ground = form.cleaned_data['gram_750_ground']
        kilogram_1_beans = form.cleaned_data['kilogram_1_beans']
        kilogram_1_ground = form.cleaned_data['kilogram_1_ground']

        total_kg_beans = request.POST['beans_total']
        total_kg_ground = request.POST['ground_total']
        total_kgs = request.POST['total_kgs']

        amount_tzs = request.POST['total_amount_tzs']
        amount_usd = request.POST['total_amount_usd']
        amount_vat_tzs = request.POST['amount_vat_tzs']
        amount_vat_usd = request.POST['amount_vat_usd']
        amount_sub_total_tzs = request.POST['amount_sub_total_tzs']
        amount_sub_total_usd = request.POST['amount_sub_total_usd']

        if(total_kgs == '0'):
            messages.warning(
                request, 'Please provide your order information!')
        else:
            Orders.objects.create(
                customer_id=customer,
                order_date=order_date,
                gram_90_beans=0 if gram_90_beans == None else gram_90_beans,
                gram_90_ground= 0 if gram_90_ground == None else gram_90_ground,
                gram_250_beans=0 if gram_250_beans == None else gram_250_beans,
                gram_250_ground=0 if gram_250_ground == None else gram_250_ground,
                gram_400_beans=0 if gram_400_beans == None else gram_400_beans,
                gram_400_ground=0 if gram_400_ground == None else gram_400_ground,
                gram_750_beans=0 if gram_750_beans == None else gram_750_beans,
                gram_750_ground=0 if gram_750_ground == None else gram_750_ground,
                kilogram_1_beans=0 if kilogram_1_beans == None else kilogram_1_beans,
                kilogram_1_ground=0 if kilogram_1_ground == None else kilogram_1_ground,
                total_kg_beans=total_kg_beans,
                total_kg_ground=total_kg_ground,
                total_kgs=total_kgs,
                amount_tzs=amount_tzs,
                amount_usd=amount_usd,
                amount_vat_tzs=amount_vat_tzs,
                amount_vat_usd=amount_vat_usd,
                amount_sub_total_tzs=amount_sub_total_tzs,
                amount_sub_total_usd=amount_sub_total_usd,
                order_status='New',
                payment_status='Not Paid'
            )
            messages.success(
                request, 'Thank you! Your order has been successfully  submitted!')
            return redirect('/order_now/')

    context = {
        'form': form,
        'title': 'Create Order',
        'company_info': company_info,
    }
    return render(request, 'customer/order_now.html', context)


@login_required
def myOrders(request):
    company_info = CompanyInfo.objects.get()
    myOrders = Orders.objects.filter(customer_id=request.user.id)
    myFilter = OrderFilters(request.GET, queryset=myOrders)
    order = myFilter.qs

    context = {
        'myOrders': myOrders,
        'title': 'My Orders',
        'myFilter': order,
        'company_info': company_info,
    }
    return render(request, 'customer/my_orders.html', context)


@login_required
def orderDetails(request, id):
    company_info = CompanyInfo.objects.get()
    orderDetails = get_object_or_404(Orders, pk=id)

    context = {
        'company_info': company_info,
        'orderDetails': orderDetails,
        'title': 'Careers Details',
    }
    return render(request, 'customer/cust_order_details.html', context)

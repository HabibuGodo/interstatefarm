from ctypes import sizeof
from email import message
import email
from email.message import Message
from xmlrpc.client import DateTime
from django.forms import DateField
import folium
from reportlab.platypus import Image
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from typing import Counter
import os
from django.contrib import auth
from django.http import response
from django.http.response import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseNotFound
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
import datetime
from django.utils.encoding import smart_str
from decimal import Decimal
from geopy.geocoders import Nominatim
import locale
locale.setlocale(locale.LC_ALL, '')
# 'en_us'


# for report lab
# End for report lab


def register(request):
    title = "User Sign Up"
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            customer_name = form.cleaned_data['customer_name']
            username = form.cleaned_data['username']
            email = email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            postal_address = form.cleaned_data['postal_address']
            pass1 = form.cleaned_data['password']
            pass2 = form.cleaned_data['password1']

            if User.objects.filter(username=username).exists():
                messages.error(request, 'The username already exists.')
            elif Customer.objects.filter(phone_number=phone_number).exists():
                messages.error(request, 'The phone number already exists.')
            elif pass1 != pass2:
                messages.error(request, 'Password do not match.')
            elif len(pass1) < 8:
                messages.error(
                    request, 'Password must be 8 or more characters.')
            else:
                # SAVE USER INTO TABLE USER
                password = make_password(pass1)
                user = User.objects.create(
                    username=username,
                    password=password,
                    email=email,
                    date_joined=datetime.datetime.now(),
                )
                # SAVE USER INTO TABLE CUSTOMER
                Customer.objects.create(
                    customer_name=customer_name,
                    postal_address=postal_address,
                    email=email,
                    phone_number=phone_number,
                    user_id=user.id,
                    visible=0,
                    added_by='Website'
                )
                messages.success(
                    request, 'Successfull created an account. Now you can login.')
                return redirect('/login/')
        else:
            print(form.errors)
    else:
        form = CustomerRegisterForm(request.POST)
        form = CustomerRegisterForm(use_required_attribute=False)

    context = {
        'title': title,
        'form': form
    }
    return render(request, 'auth/register.html', context)


def find_total():
    queryset = Stock.objects.all()

    # Calculating sum of data
    sumData = object()
    sum_of_package = 0
    sum_of_kilos = 0
    sum_of_retail_price = 0
    sum_of_wholesale_price = 0

    for dat in queryset:
        sum_of_package = sum_of_package + dat.total
        sum_of_kilos = sum_of_kilos + dat.total_kg
        sum_of_retail_price = sum_of_retail_price + dat.retail_total_price
        sum_of_wholesale_price = sum_of_wholesale_price + dat.wholesale_total_price
        sumData = {
            'sum_of_package': sum_of_package,
            'sum_of_kilos': sum_of_kilos,
            'sum_of_retail_price': sum_of_retail_price,
            'sum_of_wholesale_price': sum_of_wholesale_price
        }
    return sumData

# Create your views here.


@login_required
def dashboard(request):

    try:
        # check if user is customer
        user_type = Customer.objects.get(email=request.user.email)
    except Customer.DoesNotExist:
        user_type = None

    if user_type is not None:
        if request.user.is_active:
            return redirect('/')
        else:
            messages.error(
                request, 'Your account is not active, Contact system administrator.')
            return redirect('/login/')

    title = 'DASHBOARD'
    queryset_beans = Stock.objects.filter(package_type__contains="Beans")
    queryset_ground = Stock.objects.filter(package_type__contains="Ground")
    total_ordered_kgs = Orders.objects.aggregate(
        Sum('total_kgs')).get('total_kg__sum')
    new_ordered_kgs = Orders.objects.filter(
        order_status__contains='New').aggregate(Sum('total_kgs')).get('total_kg__sum')
    pending_ordered_kgs = Orders.objects.filter(
        order_status__contains='Pending').aggregate(Sum('total_kgs')).get('total_kg__sum')
    total_orders = Orders.objects.count()
    new_orders = Orders.objects.filter(order_status__contains='New').count()
    pending_orders = Orders.objects.filter(
        order_status__contains='Pending').count()

    sum_of_beans = 0
    sum_of_ground = 0

    # Find total beans
    for beans in queryset_beans:
        sum_of_beans = sum_of_beans + beans.total_kg

     # Find total Ground
    for ground in queryset_ground:
        sum_of_ground = sum_of_ground + ground.total_kg

    order = {
        'total_orders': total_orders,
        'new_orders': new_orders,
        'pending_orders': pending_orders,
        'total_ordered_kgs': total_ordered_kgs,
        'new_ordered_kgs': new_ordered_kgs,
        'pending_ordered_kgs': pending_ordered_kgs

    }

    context = {
        'title': title,
        'sum_of_beans': sum_of_beans,
        'sum_of_ground': sum_of_ground,
        'order': order,
        'total': find_total()
    }
    return render(request, 'staff/dashboard.html', context)

# Method to fine unit price


def unitPrice(packageType, orderData):
    our_product = PackageList.objects.get(
        package_name=packageType)
    if (orderData.total_kgs < 10):
        unit_price = our_product.retail_price
    else:
        unit_price = our_product.wholesale_price
    return unit_price


# METHOD TO CREATE PDF FILE
def createsPDF(objectData, doc_type, deni_due_date, discountValue, discountRate):
    data_file = objectData
    company_info = CompanyInfo.objects.last()

    def import_data(company_info, data_file):
        company_data = company_info
        order_data = data_file

        userdetails = get_object_or_404(User, username=order_data.customer)
        customer_ordered = Customer.objects.get(email=userdetails.email)

        # CompanyInfo
        company_name = company_data.company_name
        company_address = company_data.post_address
        tin_number = company_data.tin_number
        vrn_number = company_data.vrn_number
        company_phone = company_data.phone_number
        company_email = company_data.email_address
        region = company_data.region
        country = company_data.country
        company_website = company_data.company_website
        bank_tzs = company_data.bank_tzs
        bank_usd = company_data.bank_usd
        # for row in order_data:
        document_type = doc_type
        invoice_number = order_data.id
        invoice_date = datetime.datetime.now().strftime("%d-%m-%Y")
        customer_name = customer_ordered.customer_name
        phone_number = customer_ordered.phone_number
        email_address = customer_ordered.email

        # ================ LINE ONE

        gram_90g_alread = 0
        gram_250g_alread = 0
        gram_250b_alread = 0
        gram_400g_alread = 0
        gram_400b_alread = 0
        gram_750g_alread = 0
        gram_750b_alread = 0
        kg_1g_alread = 0
        kg_1b_alread = 0
        dripcoffee = 0

        if (order_data.gram_90_beans != 0):
            unit_price = unitPrice("90 grams - Beans", order_data)
            line_one = "90 grams - Beans"
            line_one_quantity = order_data.gram_90_beans
            line_one_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_one_total_price = locale.format(
                "%d", unit_price * order_data.gram_90_beans, grouping=True)
        elif (order_data.gram_90_ground != 0):
            gram_90g_alread = 1
            unit_price = unitPrice("90 grams - Ground", order_data)
            line_one = "90 grams - Ground"
            line_one_quantity = order_data.gram_90_ground
            line_one_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_one_total_price = locale.format(
                "%d", unit_price * order_data.gram_90_ground, grouping=True)
        elif (order_data.gram_250_beans != 0):
            gram_250b_alread = 1
            unit_price = unitPrice("250 grams - Beans", order_data)
            line_one = "250 grams - Beans"
            line_one_quantity = order_data.gram_250_beans
            line_one_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_one_total_price = locale.format(
                "%d", unit_price * order_data.gram_250_beans, grouping=True)
        elif (order_data.gram_250_ground != 0):
            gram_250g_alread = 1
            unit_price = unitPrice("250 grams - Ground", order_data)
            line_one = "250 grams - Ground"
            line_one_quantity = order_data.gram_250_ground
            line_one_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_one_total_price = locale.format(
                "%d", unit_price * order_data.gram_250_ground, grouping=True)
        elif (order_data.gram_400_beans != 0):
            gram_400b_alread = 1
            unit_price = unitPrice("400 grams - Beans", order_data)
            line_one = "400 grams - Beans"
            line_one_quantity = order_data.gram_400_beans
            line_one_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_one_total_price = locale.format(
                "%d", unit_price * order_data.gram_400_beans, grouping=True)
        elif (order_data.gram_400_ground != 0):
            gram_400g_alread = 1
            unit_price = unitPrice("400 grams - Ground", order_data)
            line_one = "400 grams - Ground"
            line_one_quantity = order_data.gram_400_ground
            line_one_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_one_total_price = locale.format(
                "%d", unit_price * order_data.gram_400_ground, grouping=True)
        elif (order_data.gram_750_beans != 0):
            gram_750b_alread = 1
            unit_price = unitPrice("750 grams - Beans", order_data)
            line_one = "750 grams - Beans"
            line_one_quantity = order_data.gram_750_beans
            line_one_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_one_total_price = locale.format(
                "%d",  unit_price * order_data.gram_750_beans, grouping=True)
        elif (order_data.gram_750_ground != 0):
            gram_750g_alread = 1
            unit_price = unitPrice("750 grams - Ground", order_data)
            line_one = "750 grams - Ground"
            line_one_quantity = order_data.gram_750_ground
            line_one_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_one_total_price = locale.format(
                "%d", unit_price * order_data.gram_750_ground, grouping=True)
        elif (order_data.kilogram_1_beans != 0):
            kg_1b_alread = 1
            unit_price = unitPrice("1 kilogram - Beans", order_data)
            line_one = "1 kilogram - Beans"
            line_one_quantity = order_data.kilogram_1_beans
            line_one_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_one_total_price = locale.format(
                "%d", unit_price * order_data.kilogram_1_beans, grouping=True)
        elif (order_data.kilogram_1_ground != 0):
            kg_1g_alread = 1
            unit_price = unitPrice("1 kilogram - Ground", order_data)
            line_one = "1 kilogram - Ground"
            line_one_quantity = order_data.kilogram_1_ground
            line_one_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_one_total_price = locale.format(
                "%d", unit_price * order_data.kilogram_1_ground, grouping=True)
        else:
            dripcoffee = 1
            unit_price = unitPrice("Drip Coffee", order_data)
            line_one = "Drip Coffee"
            line_one_quantity = order_data.drip_coffee
            line_one_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_one_total_price = locale.format(
                "%d", unit_price * order_data.drip_coffee, grouping=True)

        # ====================LINE TWO
        if (order_data.gram_90_ground != 0 and gram_90g_alread != 1):
            gram_90g_alread = 1
            unit_price = unitPrice("90 grams - Ground", order_data)
            line_two = "90 grams - Ground"
            line_two_quantity = order_data.gram_90_ground
            line_two_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_two_total_price = locale.format(
                "%d", unit_price * order_data.gram_90_ground, grouping=True)
        elif (order_data.gram_250_beans != 0 and gram_250b_alread != 1):
            gram_250b_alread = 1
            unit_price = unitPrice("250 grams - Beans", order_data)
            line_two = "250 grams - Beans"
            line_two_quantity = order_data.gram_250_beans
            line_two_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_two_total_price = locale.format(
                "%d", unit_price * order_data.gram_250_beans, grouping=True)
        elif (order_data.gram_250_ground != 0 and gram_250g_alread != 1):
            gram_250g_alread = 1
            unit_price = unitPrice("250 grams - Ground", order_data)
            line_two = "250 grams - Ground"
            line_two_quantity = order_data.gram_250_ground
            line_two_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_two_total_price = locale.format(
                "%d", unit_price * order_data.gram_250_ground, grouping=True)
        elif (order_data.gram_400_beans != 0 and gram_400b_alread != 1):
            gram_400b_alread = 1
            unit_price = unitPrice("400 grams - Beans", order_data)
            line_two = "400 grams - Beans"
            line_two_quantity = order_data.gram_400_beans
            line_two_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_two_total_price = locale.format(
                "%d", unit_price * order_data.gram_400_beans, grouping=True)
        elif (order_data.gram_400_ground != 0 and gram_400g_alread != 1):
            gram_400g_alread = 1
            unit_price = unitPrice("400 grams - Ground", order_data)
            line_two = "400 grams - Ground"
            line_two_quantity = order_data.gram_400_ground
            line_two_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_two_total_price = locale.format(
                "%d", unit_price * order_data.gram_400_ground, grouping=True)
        elif (order_data.gram_750_beans != 0 and gram_750b_alread != 1):
            gram_750b_alread = 1
            unit_price = unitPrice("750 grams - Beans", order_data)
            line_two = "750 grams - Beans"
            line_two_quantity = order_data.gram_750_beans
            line_two_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_two_total_price = locale.format(
                "%d",  unit_price * order_data.gram_750_beans, grouping=True)
        elif (order_data.gram_750_ground != 0 and gram_750g_alread != 1):
            gram_750g_alread = 1
            unit_price = unitPrice("750 grams - Ground", order_data)
            line_two = "750 grams - Ground"
            line_two_quantity = order_data.gram_750_ground
            line_two_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_two_total_price = locale.format(
                "%d", unit_price * order_data.gram_750_ground, grouping=True)
        elif (order_data.kilogram_1_beans != 0 and kg_1b_alread != 1):
            kg_1b_alread = 1
            unit_price = unitPrice("1 kilogram - Beans", order_data)
            line_two = "1 kilogram - Beans"
            line_two_quantity = order_data.kilogram_1_beans
            line_two_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_two_total_price = locale.format(
                "%d", unit_price * order_data.kilogram_1_beans, grouping=True)
        elif (order_data.kilogram_1_ground != 0 and kg_1g_alread != 1):
            kg_1g_alread = 1
            unit_price = unitPrice("1 kilogram - Ground", order_data)
            line_two = "1 kilogram - Ground"
            line_two_quantity = order_data.kilogram_1_ground
            line_two_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_two_total_price = locale.format(
                "%d", unit_price * order_data.kilogram_1_ground, grouping=True)
        else:
            line_two = ""
            line_two_quantity = ''
            line_two_unit_price = ''
            line_two_total_price = ''

            line_three = ""
            line_three_quantity = ''
            line_three_unit_price = ''
            line_three_total_price = ''

            line_four = ""
            line_four_quantity = ''
            line_four_unit_price = ''
            line_four_total_price = ''
            line_five = ""
            line_five_quantity = ''
            line_five_unit_price = ''
            line_five_total_price = ''
            line_six = ""
            line_six_quantity = ''
            line_six_unit_price = ''
            line_six_total_price = ''
            line_seven = ""
            line_seven_quantity = ''
            line_seven_unit_price = ''
            line_seven_total_price = ''
            line_eight = ""
            line_eight_quantity = ''
            line_eight_unit_price = ''
            line_eight_total_price = ''
            line_nine = ""
            line_nine_quantity = ''
            line_nine_unit_price = ''
            line_nine_total_price = ''
            line_ten = ""
            line_ten_quantity = ''
            line_ten_unit_price = ''
            line_ten_total_price = ''

        # =============LINE THREE
        if (order_data.gram_250_beans != 0 and gram_250b_alread != 1):
            gram_250b_alread = 1
            unit_price = unitPrice("250 grams - Beans", order_data)
            line_three = "250 grams - Beans"
            line_three_quantity = order_data.gram_250_beans
            line_three_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_three_total_price = locale.format(
                "%d", unit_price * order_data.gram_250_beans, grouping=True)
        elif (order_data.gram_250_ground != 0 and gram_250g_alread != 1):
            gram_250g_alread = 1
            unit_price = unitPrice("250 grams - Ground", order_data)
            line_three = "250 grams - Ground"
            line_three_quantity = order_data.gram_250_ground
            line_three_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_three_total_price = locale.format(
                "%d", unit_price * order_data.gram_250_ground, grouping=True)
        elif (order_data.gram_400_beans != 0 and gram_400b_alread != 1):
            gram_400b_alread = 1
            unit_price = unitPrice("400 grams - Beans", order_data)
            line_three = "400 grams - Beans"
            line_three_quantity = order_data.gram_400_beans
            line_three_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_three_total_price = locale.format(
                "%d", unit_price * order_data.gram_400_beans, grouping=True)
        elif (order_data.gram_400_ground != 0 and gram_400g_alread != 1):
            gram_400g_alread = 1
            unit_price = unitPrice("400 grams - Ground", order_data)
            line_three = "400 grams - Ground"
            line_three_quantity = order_data.gram_400_ground
            line_three_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_three_total_price = locale.format(
                "%d", unit_price * order_data.gram_400_ground, grouping=True)
        elif (order_data.gram_750_beans != 0 and gram_750b_alread != 1):
            gram_750b_alread = 1
            unit_price = unitPrice("750 grams - Beans", order_data)
            line_three = "750 grams - Beans"
            line_three_quantity = order_data.gram_750_beans
            line_three_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_three_total_price = locale.format(
                "%d",  unit_price * order_data.gram_750_beans, grouping=True)
        elif (order_data.gram_750_ground != 0 and gram_750g_alread != 1):
            gram_750g_alread = 1
            unit_price = unitPrice("750 grams - Ground", order_data)
            line_three = "750 grams - Ground"
            line_three_quantity = order_data.gram_750_ground
            line_three_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_three_total_price = locale.format(
                "%d", unit_price * order_data.gram_750_ground, grouping=True)
        elif (order_data.kilogram_1_beans != 0 and kg_1b_alread != 1):
            kg_1b_alread = 1
            unit_price = unitPrice("1 kilogram - Beans", order_data)
            line_three = "1 kilogram - Beans"
            line_three_quantity = order_data.kilogram_1_beans
            line_three_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_three_total_price = locale.format(
                "%d", unit_price * order_data.kilogram_1_beans, grouping=True)
        elif (order_data.kilogram_1_ground != 0 and kg_1g_alread != 1):
            kg_1g_alread = 1
            unit_price = unitPrice("1 kilogram - Ground", order_data)
            line_three = "1 kilogram - Ground"
            line_three_quantity = order_data.kilogram_1_ground
            line_three_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_three_total_price = locale.format(
                "%d", unit_price * order_data.kilogram_1_ground, grouping=True)
        else:
            line_three = ""
            line_three_quantity = ''
            line_three_unit_price = ''
            line_three_total_price = ''
            line_four = ""
            line_four_quantity = ''
            line_four_unit_price = ''
            line_four_total_price = ''
            line_five = ""
            line_five_quantity = ''
            line_five_unit_price = ''
            line_five_total_price = ''
            line_six = ""
            line_six_quantity = ''
            line_six_unit_price = ''
            line_six_total_price = ''
            line_seven = ""
            line_seven_quantity = ''
            line_seven_unit_price = ''
            line_seven_total_price = ''
            line_eight = ""
            line_eight_quantity = ''
            line_eight_unit_price = ''
            line_eight_total_price = ''
            line_nine = ""
            line_nine_quantity = ''
            line_nine_unit_price = ''
            line_nine_total_price = ''
            line_ten = ""
            line_ten_quantity = ''
            line_ten_unit_price = ''
            line_ten_total_price = ''

        # ==========LINE FOUR
        if (order_data.gram_250_ground != 0 and gram_250g_alread != 1):
            gram_250g_alread = 1
            unit_price = unitPrice("250 grams - Ground", order_data)
            line_four = "250 grams - Ground"
            line_four_quantity = order_data.gram_250_ground
            line_four_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_four_total_price = locale.format(
                "%d", unit_price * order_data.gram_250_ground, grouping=True)
        elif (order_data.gram_400_beans != 0 and gram_400b_alread != 1):
            gram_400b_alread = 1
            unit_price = unitPrice("400 grams - Beans", order_data)
            line_four = "400 grams - Beans"
            line_four_quantity = order_data.gram_400_beans
            line_four_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_four_total_price = locale.format(
                "%d", unit_price * order_data.gram_400_beans, grouping=True)
        elif (order_data.gram_400_ground != 0 and gram_400g_alread != 1):
            gram_400g_alread = 1
            unit_price = unitPrice("400 grams - Ground", order_data)
            line_four = "400 grams - Ground"
            line_four_quantity = order_data.gram_400_ground
            line_four_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_four_total_price = locale.format(
                "%d", unit_price * order_data.gram_400_ground, grouping=True)
        elif (order_data.gram_750_beans != 0 and gram_750b_alread != 1):
            gram_750b_alread = 1
            unit_price = unitPrice("750 grams - Beans", order_data)
            line_four = "750 grams - Beans"
            line_four_quantity = order_data.gram_750_beans
            line_four_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_four_total_price = locale.format(
                "%d",  unit_price * order_data.gram_750_beans, grouping=True)
        elif (order_data.gram_750_ground != 0 and gram_750g_alread != 1):
            gram_750g_alread = 1
            unit_price = unitPrice("750 grams - Ground", order_data)
            line_four = "750 grams - Ground"
            line_four_quantity = order_data.gram_750_ground
            line_four_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_four_total_price = locale.format(
                "%d", unit_price * order_data.gram_750_ground, grouping=True)
        elif (order_data.kilogram_1_beans != 0 and kg_1b_alread != 1):
            kg_1b_alread = 1
            unit_price = unitPrice("1 kilogram - Beans", order_data)
            line_four = "1 kilogram - Beans"
            line_four_quantity = order_data.kilogram_1_beans
            line_four_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_four_total_price = locale.format(
                "%d", unit_price * order_data.kilogram_1_beans, grouping=True)
        elif (order_data.kilogram_1_ground != 0 and kg_1g_alread != 1):
            kg_1g_alread = 1
            unit_price = unitPrice("1 kilogram - Ground", order_data)
            line_four = "1 kilogram - Ground"
            line_four_quantity = order_data.kilogram_1_ground
            line_four_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_four_total_price = locale.format(
                "%d", unit_price * order_data.kilogram_1_ground, grouping=True)
        else:
            line_four = ""
            line_four_quantity = ''
            line_four_unit_price = ''
            line_four_total_price = ''
            line_five = ""
            line_five_quantity = ''
            line_five_unit_price = ''
            line_five_total_price = ''
            line_six = ""
            line_six_quantity = ''
            line_six_unit_price = ''
            line_six_total_price = ''
            line_seven = ""
            line_seven_quantity = ''
            line_seven_unit_price = ''
            line_seven_total_price = ''
            line_eight = ""
            line_eight_quantity = ''
            line_eight_unit_price = ''
            line_eight_total_price = ''
            line_nine = ""
            line_nine_quantity = ''
            line_nine_unit_price = ''
            line_nine_total_price = ''
            line_ten = ""
            line_ten_quantity = ''
            line_ten_unit_price = ''
            line_ten_total_price = ''

        # ================ LINE 5
        if (order_data.gram_400_beans != 0 and gram_400b_alread != 1):
            gram_400b_alread = 1
            unit_price = unitPrice("400 grams - Beans", order_data)
            line_five = "400 grams - Beans"
            line_five_quantity = order_data.gram_400_beans
            line_five_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_five_total_price = locale.format(
                "%d", unit_price * order_data.gram_400_beans, grouping=True)
        elif (order_data.gram_400_ground != 0 and gram_400g_alread != 1):
            gram_400g_alread = 1
            unit_price = unitPrice("400 grams - Ground", order_data)
            line_five = "400 grams - Ground"
            line_five_quantity = order_data.gram_400_ground
            line_five_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_five_total_price = locale.format(
                "%d", unit_price * order_data.gram_400_ground, grouping=True)
        elif (order_data.gram_750_beans != 0 and gram_750b_alread != 1):
            gram_750b_alread = 1
            unit_price = unitPrice("750 grams - Beans", order_data)
            line_five = "750 grams - Beans"
            line_five_quantity = order_data.gram_750_beans
            line_five_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_five_total_price = locale.format(
                "%d",  unit_price * order_data.gram_750_beans, grouping=True)
        elif (order_data.gram_750_ground != 0 and gram_750g_alread != 1):
            gram_750g_alread = 1
            unit_price = unitPrice("750 grams - Ground", order_data)
            line_five = "750 grams - Ground"
            line_five_quantity = order_data.gram_750_ground
            line_five_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_five_total_price = locale.format(
                "%d", unit_price * order_data.gram_750_ground, grouping=True)
        elif (order_data.kilogram_1_beans != 0 and kg_1b_alread != 1):
            kg_1b_alread = 1
            unit_price = unitPrice("1 kilogram - Beans", order_data)
            line_five = "1 kilogram - Beans"
            line_five_quantity = order_data.kilogram_1_beans
            line_five_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_five_total_price = locale.format(
                "%d", unit_price * order_data.kilogram_1_beans, grouping=True)
        elif (order_data.kilogram_1_ground != 0 and kg_1g_alread != 1):
            kg_1g_alread = 1
            unit_price = unitPrice("1 kilogram - Ground", order_data)
            line_five = "1 kilogram - Ground"
            line_five_quantity = order_data.kilogram_1_ground
            line_five_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_five_total_price = locale.format(
                "%d", unit_price * order_data.kilogram_1_ground, grouping=True)
        else:
            line_five = ""
            line_five_quantity = ''
            line_five_unit_price = ''
            line_five_total_price = ''
            line_six = ""
            line_six_quantity = ''
            line_six_unit_price = ''
            line_six_total_price = ''
            line_seven = ""
            line_seven_quantity = ''
            line_seven_unit_price = ''
            line_seven_total_price = ''
            line_eight = ""
            line_eight_quantity = ''
            line_eight_unit_price = ''
            line_eight_total_price = ''
            line_nine = ""
            line_nine_quantity = ''
            line_nine_unit_price = ''
            line_nine_total_price = ''
            line_ten = ""
            line_ten_quantity = ''
            line_ten_unit_price = ''
            line_ten_total_price = ''

        # =================LINE SIX
        if (order_data.gram_400_ground != 0 and gram_400g_alread != 1):
            gram_400g_alread = 1
            unit_price = unitPrice("400 grams - Ground", order_data)
            line_six = "400 grams - Ground"
            line_six_quantity = order_data.gram_400_ground
            line_six_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_six_total_price = locale.format(
                "%d", unit_price * order_data.gram_400_ground, grouping=True)
        elif (order_data.gram_750_beans != 0 and gram_750b_alread != 1):
            gram_750b_alread = 1
            unit_price = unitPrice("750 grams - Beans", order_data)
            line_six = "750 grams - Beans"
            line_six_quantity = order_data.gram_750_beans
            line_six_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_six_total_price = locale.format(
                "%d",  unit_price * order_data.gram_750_beans, grouping=True)
        elif (order_data.gram_750_ground != 0 and gram_750g_alread != 1):
            gram_750g_alread = 1
            unit_price = unitPrice("750 grams - Ground", order_data)
            line_six = "750 grams - Ground"
            line_six_quantity = order_data.gram_750_ground
            line_six_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_six_total_price = locale.format(
                "%d", unit_price * order_data.gram_750_ground, grouping=True)
        elif (order_data.kilogram_1_beans != 0 and kg_1b_alread != 1):
            kg_1b_alread = 1
            unit_price = unitPrice("1 kilogram - Beans", order_data)
            line_six = "1 kilogram - Beans"
            line_six_quantity = order_data.kilogram_1_beans
            line_six_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_six_total_price = locale.format(
                "%d", unit_price * order_data.kilogram_1_beans, grouping=True)
        elif (order_data.kilogram_1_ground != 0 and kg_1g_alread != 1):
            kg_1g_alread = 1
            unit_price = unitPrice("1 kilogram - Ground", order_data)
            line_six = "1 kilogram - Ground"
            line_six_quantity = order_data.kilogram_1_ground
            line_six_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_six_total_price = locale.format(
                "%d", unit_price * order_data.kilogram_1_ground, grouping=True)
        else:
            line_six = ""
            line_six_quantity = ''
            line_six_unit_price = ''
            line_six_total_price = ''
            line_seven = ""
            line_seven_quantity = ''
            line_seven_unit_price = ''
            line_seven_total_price = ''
            line_eight = ""
            line_eight_quantity = ''
            line_eight_unit_price = ''
            line_eight_total_price = ''
            line_nine = ""
            line_nine_quantity = ''
            line_nine_unit_price = ''
            line_nine_total_price = ''
            line_ten = ""
            line_ten_quantity = ''
            line_ten_unit_price = ''
            line_ten_total_price = ''

        # ==============LINE SEVEN
        if (order_data.gram_750_beans != 0 and gram_750b_alread != 1):
            gram_750b_alread = 1
            unit_price = unitPrice("750 grams - Beans", order_data)
            line_seven = "750 grams - Beans"
            line_seven_quantity = order_data.gram_750_beans
            line_seven_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_seven_total_price = locale.format(
                "%d",  unit_price * order_data.gram_750_beans, grouping=True)
        elif (order_data.gram_750_ground != 0 and gram_750g_alread != 1):
            gram_750g_alread = 1
            unit_price = unitPrice("750 grams - Ground", order_data)
            line_seven = "750 grams - Ground"
            line_seven_quantity = order_data.gram_750_ground
            line_seven_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_seven_total_price = locale.format(
                "%d", unit_price * order_data.gram_750_ground, grouping=True)
        elif (order_data.kilogram_1_beans != 0 and kg_1b_alread != 1):
            kg_1b_alread = 1
            unit_price = unitPrice("1 kilogram - Beans", order_data)
            line_seven = "1 kilogram - Beans"
            line_seven_quantity = order_data.kilogram_1_beans
            line_seven_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_seven_total_price = locale.format(
                "%d", unit_price * order_data.kilogram_1_beans, grouping=True)
        elif (order_data.kilogram_1_ground != 0 and kg_1g_alread != 1):
            kg_1g_alread = 1
            unit_price = unitPrice("1 kilogram - Ground", order_data)
            line_seven = "1 kilogram - Ground"
            line_seven_quantity = order_data.kilogram_1_ground
            line_seven_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_seven_total_price = locale.format(
                "%d", unit_price * order_data.kilogram_1_ground, grouping=True)
        else:
            line_seven = ""
            line_seven_quantity = ''
            line_seven_unit_price = ''
            line_seven_total_price = ''
            line_eight = ""
            line_eight_quantity = ''
            line_eight_unit_price = ''
            line_eight_total_price = ''
            line_nine = ""
            line_nine_quantity = ''
            line_nine_unit_price = ''
            line_nine_total_price = ''
            line_ten = ""
            line_ten_quantity = ''
            line_ten_unit_price = ''
            line_ten_total_price = ''

        # ====================LINE EIGHT
        if (order_data.gram_750_ground != 0 and gram_750g_alread != 1):
            gram_750g_alread = 1
            unit_price = unitPrice("750 grams - Ground", order_data)
            line_eight = "750 grams - Ground"
            line_eight_quantity = order_data.gram_750_ground
            line_eight_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_eight_total_price = locale.format(
                "%d", unit_price * order_data.gram_750_ground, grouping=True)
        elif (order_data.kilogram_1_beans != 0 and kg_1b_alread != 1):
            kg_1b_alread = 1
            unit_price = unitPrice("1 kilogram - Beans", order_data)
            line_eight = "1 kilogram - Beans"
            line_eight_quantity = order_data.kilogram_1_beans
            line_eight_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_eight_total_price = locale.format(
                "%d", unit_price * order_data.kilogram_1_beans, grouping=True)
        elif (order_data.kilogram_1_ground != 0 and kg_1g_alread != 1):
            kg_1g_alread = 1
            unit_price = unitPrice("1 kilogram - Ground", order_data)
            line_eight = "1 kilogram - Ground"
            line_eight_quantity = order_data.kilogram_1_ground
            line_eight_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_eight_total_price = locale.format(
                "%d", unit_price * order_data.kilogram_1_ground, grouping=True)
        else:
            line_eight = ""
            line_eight_quantity = ''
            line_eight_unit_price = ''
            line_eight_total_price = ''
            line_nine = ""
            line_nine_quantity = ''
            line_nine_unit_price = ''
            line_nine_total_price = ''
            line_ten = ""
            line_ten_quantity = ''
            line_ten_unit_price = ''
            line_ten_total_price = ''

        # ==============LINE NINE
        if (order_data.kilogram_1_beans != 0 and kg_1b_alread != 1):
            kg_1b_alread = 1
            unit_price = unitPrice("1 kilogram - Beans", order_data)
            line_nine = "1 kilogram - Beans"
            line_nine_quantity = order_data.kilogram_1_beans
            line_nine_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_nine_total_price = locale.format(
                "%d", unit_price * order_data.kilogram_1_beans, grouping=True)
        elif (order_data.kilogram_1_ground != 0 and kg_1g_alread != 1):
            kg_1g_alread = 1
            unit_price = unitPrice("1 kilogram - Ground", order_data)
            line_nine = "1 kilogram - Ground"
            line_nine_quantity = order_data.kilogram_1_ground
            line_nine_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_nine_total_price = locale.format(
                "%d", unit_price * order_data.kilogram_1_ground, grouping=True)
        else:
            line_nine = ""
            line_nine_quantity = ''
            line_nine_unit_price = ''
            line_nine_total_price = ''
            line_ten = ""
            line_ten_quantity = ''
            line_ten_unit_price = ''
            line_ten_total_price = ''

        # ==================LINE TEN
        if (order_data.kilogram_1_ground != 0 and kg_1g_alread != 1):
            kg_1g_alread = 1
            unit_price = unitPrice("1 kilogram - Ground", order_data)
            line_ten = "1 kilogram - Ground"
            line_ten_quantity = order_data.kilogram_1_ground
            line_ten_unit_price = locale.format(
                "%d", unit_price, grouping=True)
            line_ten_total_price = locale.format(
                "%d", unit_price * order_data.kilogram_1_ground, grouping=True)
        else:
            line_ten = ""
            line_ten_quantity = ''
            line_ten_unit_price = ''
            line_ten_total_price = ''

        discount_rate = float(discountRate)
        discount = discountValue

        sub_total = locale.format(
            "%d", order_data.amount_sub_total_tzs, grouping=True)
        tax = locale.format(
            "%d", order_data.amount_vat_tzs, grouping=True)

        total = order_data.amount_tzs

        pdf_file_name = str(invoice_number) + '_' + \
            str(customer_name)+'_'+document_type + '.pdf'
        fullpath=os.path.abspath(os.path.expanduser("~/Downloads/"+pdf_file_name))
        # file_path_name = os.path.join(os.path.expanduser("~"), "Downloads/", pdf_file_name)
        generate_invoice(
            str(company_name), str(company_address), str(tin_number),
            str(vrn_number), str(company_phone), str(company_email),
            str(region), str(country), str(company_website),
            str(bank_tzs), str(bank_usd),
            str(customer_name), str(invoice_number),
            str(line_one), str(line_one_quantity), str(
                line_one_unit_price),
            str(line_one_total_price),
            str(
                line_two), str(line_two_quantity),
            str(line_two_unit_price), str(
                line_two_total_price),
            str(line_three),
            str(line_three_quantity), str(line_three_unit_price),
            str(line_three_total_price),
            str(
                line_four), str(line_four_quantity),
            str(line_four_unit_price), str(
                line_four_total_price),
            str(line_five),
            str(line_five_quantity), str(line_five_unit_price),
            str(line_five_total_price),
            str(
                line_six), str(line_six_quantity),
            str(line_six_unit_price), str(
                line_six_total_price),
            str(line_seven),
            str(line_seven_quantity), str(line_seven_unit_price),
            str(line_seven_total_price),
            str(
                line_eight), str(line_eight_quantity),
            str(line_eight_unit_price), str(
                line_eight_total_price),
            str(
                line_nine), str(line_nine_quantity),
            str(line_nine_unit_price), str(
                line_nine_total_price),
            str(line_ten), str(line_ten_quantity),
            str(line_ten_unit_price), str(
                line_ten_total_price),

            str(discount_rate),
            str(discount),
            str(sub_total),
            str(tax),

            str(total),
            str(
                email_address), str(
                phone_number), str(invoice_date),
            str(document_type), deni_due_date,fullpath)
    def generate_invoice(company_name, company_address, tin_number, vrn_number, company_phone,
                         company_email, region, country, company_website, bank_tzs, bank_usd, customer_name, invoice_number,
                         line_one, line_one_quantity, line_one_unit_price, line_one_total_price,
                         line_two, line_two_quantity, line_two_unit_price, line_two_total_price,
                         line_three, line_three_quantity, line_three_unit_price, line_three_total_price,
                         line_four, line_four_quantity, line_four_unit_price, line_four_total_price,
                         line_five, line_five_quantity, line_five_unit_price, line_five_total_price,
                         line_six, line_six_quantity, line_six_unit_price, line_six_total_price,
                         line_seven, line_seven_quantity, line_seven_unit_price, line_seven_total_price,
                         line_eight, line_eight_quantity, line_eight_unit_price, line_eight_total_price,
                         line_nine, line_nine_quantity, line_nine_unit_price, line_nine_total_price,
                         line_ten, line_ten_quantity, line_ten_unit_price, line_ten_total_price,
                         discount_rate, discount,
                         sub_total, tax, total,
                         email_address, phone_number, invoice_date, document_type, deni_due_date,file_path):
        c = canvas.Canvas(file_path, pagesize=letter)

        # image of seal
        logo = 'interstate_logo.png'
        c.drawImage(logo, 50, 700, width=140, height=110)

        c.setFont('Helvetica-Bold', 20, leading=None)
        c.setFillColor('green')
        c.drawCentredString(430, 700, str(document_type))

        # RIGHT INFO
        c.setFillColor('black')
        c.setFont('Helvetica', 11, leading=None)
        c.drawCentredString(400, 660, str(document_type) + '#:')
        c.setFont('Helvetica-Bold', 11, leading=None)
        invoice_number_string = str('0000-' + invoice_number)
        c.drawCentredString(480, 660, invoice_number_string)
        c.setFont('Helvetica', 11, leading=None)
        c.drawCentredString(425, 645, "TIN:")
        c.drawCentredString(483, 645, tin_number)
        c.drawCentredString(422, 630, "VRN:")
        c.drawCentredString(484, 630, vrn_number)
        c.drawCentredString(420, 615, "DATE:")
        c.drawCentredString(481, 615, invoice_date)

        # Company Address
        c.drawString(58, 660, company_name)
        c.drawString(58, 645, "P.O Box "+company_address)
        c.drawString(58, 630, region+', '+country)
        c.drawString(58, 615, company_phone)
        c.drawString(58, 600, company_email)
        c.drawString(58, 585, company_website)

        # Customer info
        c.setFont('Helvetica-Bold', 12, leading=None)
        c.drawCentredString(71, 560, "TO:")
        c.setFont('Helvetica', 12, leading=None)
        c.drawCentredString(130, 558, '______________________')
        c.setFont('Helvetica', 11, leading=None)
        c.drawString(58, 543, customer_name)
        c.drawString(58, 528, phone_number)
        c.drawString(58, 513, email_address)

        c.setFont('Helvetica', 12, leading=None)
        # c.drawCentredString(320, 500, "Particulars:")

        c.drawCentredString(
            295, 488, "________________________________________________________________________")
        c.drawCentredString(
            295, 468, "________________________________________________________________________")
        c.drawCentredString(
            295, 448, "________________________________________________________________________")
        c.drawCentredString(
            295, 428, "________________________________________________________________________")
        c.drawCentredString(
            295, 408, "________________________________________________________________________")
        c.drawCentredString(
            295, 388, "________________________________________________________________________")
        c.drawCentredString(
            295, 368, "________________________________________________________________________")
        c.drawCentredString(
            295, 348, "________________________________________________________________________")
        c.drawCentredString(
            295, 328, "________________________________________________________________________")
        c.drawCentredString(
            295, 308, "________________________________________________________________________")
        c.drawCentredString(
            295, 288, "________________________________________________________________________")

        c.setFont('Helvetica-Bold', 11, leading=None)
        c.drawString(58, 490, 'DESCRIPTION')
        c.drawCentredString(240, 490, 'QTY')
        c.drawCentredString(350, 490, 'UNIT PRICE')
        c.drawCentredString(490, 490, 'LINE TOTAL')

        c.setFont('Helvetica', 11, leading=None)
        c.drawString(58, 473, line_one)
        c.drawCentredString(240, 473, line_one_quantity)
        c.drawCentredString(350, 473, line_one_unit_price)
        c.drawCentredString(490, 473, line_one_total_price)

        c.drawString(58, 453, line_two)
        c.drawCentredString(240, 453, line_two_quantity)
        c.drawCentredString(350, 453, line_two_unit_price)
        c.drawCentredString(490, 453, line_two_total_price)

        c.drawString(58, 433, line_three)
        c.drawCentredString(240, 433, line_three_quantity)
        c.drawCentredString(350, 433, line_three_unit_price)
        c.drawCentredString(490, 433, line_three_total_price)

        c.drawString(58, 413, line_four)
        c.drawCentredString(240, 413, line_four_quantity)
        c.drawCentredString(350, 413, line_four_unit_price)
        c.drawCentredString(490, 413, line_four_total_price)

        c.drawString(58, 393, line_five)
        c.drawCentredString(240, 393, line_five_quantity)
        c.drawCentredString(350, 393, line_five_unit_price)
        c.drawCentredString(490, 393, line_five_total_price)

        c.drawString(58, 373, line_six)
        c.drawCentredString(240, 373, line_six_quantity)
        c.drawCentredString(350, 373, line_six_unit_price)
        c.drawCentredString(490, 373, line_six_total_price)

        c.drawString(58, 353, line_seven)
        c.drawCentredString(240, 353, line_seven_quantity)
        c.drawCentredString(350, 353, line_seven_unit_price)
        c.drawCentredString(490, 353, line_seven_total_price)

        c.drawString(58, 333, line_eight)
        c.drawCentredString(240, 333, line_eight_quantity)
        c.drawCentredString(350, 333, line_eight_unit_price)
        c.drawCentredString(490, 333, line_eight_total_price)

        c.drawString(58, 313, line_nine)
        c.drawCentredString(240, 313, line_nine_quantity)
        c.drawCentredString(350, 313, line_nine_unit_price)
        c.drawCentredString(490, 313, line_nine_total_price)

        c.drawString(58, 293, line_ten)
        c.drawCentredString(240, 293, line_ten_quantity)
        c.drawCentredString(350, 293, line_ten_unit_price)
        c.drawCentredString(490, 293, line_ten_total_price)

        if(doc_type != 'Receipt'):
            # Instructions
            c.setFont('Helvetica-Bold', 11, leading=None)
            c.drawString(58, 233, 'Bank Name : CRDB Bank Plc,')
            c.drawString(
                58, 218, "Remarks / Payment Instructions:")
            c.setFont('Helvetica', 11, leading=None)
            c.drawString(
                58, 203, '1. Total payment due is '+str(deni_due_date.strftime("(%d %B, %Y)")))
            c.drawString(
                58, 188, '2. Please include the invoice number on your check')

            c.drawString(
                58, 173, 'Account Name : Inter State Farm Company Limited')
            c.drawString(
                58, 158, 'Account Number : '+bank_tzs + ' - TZS')
            c.drawString(58, 143, 'Branch Name : Mbinga')
            c.drawString(58, 128, 'Swiftcode : CORUTZTZ')

        # SUB TOTAL
        c.setFont('Helvetica', 11, leading=None)
        c.drawString(398, 220, "SUB-TOTAL: "+sub_total+"TZS")

        # VAT
        c.setFont('Helvetica', 11, leading=None)
        c.drawString(405, 200, "VAT (18%): "+tax+"TZS")

        # DISCOUNT
        c.setFont('Helvetica', 11, leading=None)
        c.drawString(
            375, 180, "DISCOUNT ("+str(round(float(discount_rate), 1))+"%): ")
        c.drawString(478, 180, locale.format(
            "%d", (round(float(discount), 1)), grouping=True)+"TZS")

        # TOTAL

        total_cost = locale.format(
            "%d", (float(total) - float(discount)), grouping=True)
        c.setFont('Helvetica-Bold', 11, leading=None)
        c.drawString(423, 160, "TOTAL: "+total_cost+'TZS')

        # SIGN

        if(doc_type != 'Receipt'):

            c.setFont('Helvetica-Bold', 12, leading=None)
            c.drawString(58, 90, "__________________")
            c.setFont('Helvetica-Bold', 12, leading=None)
            c.drawString(73, 70, 'Finance Officer')
        else:
            c.setFont('Helvetica-Bold', 12, leading=None)
            c.drawString(58, 173, "__________________")
            c.setFont('Helvetica-Bold', 12, leading=None)
            c.drawString(73, 158, 'Finance Officer')

        c.setFont('Helvetica-Bold', 12, leading=None)
        c.drawCentredString(320, 30, 'Thank You For Your Business!')

        c.showPage()
        c.save()
        
        return response

    import_data(company_info, data_file)



@login_required
def all_invoices(request):
    if request.user.is_staff != 1:
        return HttpResponseNotFound("<h1>Error 404: Access to this page is restricted<h1>")
    title = "Invoices"
    queryset = Invoice.objects.all().order_by('-invoice_date')


    totalpaid = 0
    total = 0
    dat = []

    for allInvoice in queryset:
        paymentInfo = Payments.objects.filter(order_number=allInvoice.invoice_number)
        for paidAmount in paymentInfo:
            total = total + paidAmount.paid_amount_tzs 
        totalpaid = total
        dat.append(totalpaid)
        total = 0 


    context = {
        'title': title,
        'queryset': queryset,
        'totalpaid':dat
    }
    return render(request, 'staff/all_invoices.html', context)

# INVOICE UPDATION


@login_required
def createInvoice(request, pk):

    if request.user.is_staff != 1:
        return HttpResponseNotFound("<h1>Error 404: Access to this page is restricted<h1>")
    # select data based on primary key
    orderDetails = Orders.objects.get(id=pk)
    if(orderDetails.order_status == 'New'):
        doc_type = "Tax Invoice"
    else:
        doc_type = "Receipt"
    today = datetime.date.today()

    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            discount_type = form.cleaned_data['discount_type']
            discountValue = form.cleaned_data['discount']
            discount_rate = form.cleaned_data['discount_rate']

            
            if(orderDetails.amount_tzs <= 350000):
                deni_due_date = today + datetime.timedelta(days=14)
            else:
                deni_due_date = today + datetime.timedelta(days=30)
            try:
                fetchCustomer = Customer.objects.get(
                    user_id=orderDetails.customer_id)
                # return HttpResponse(fetchCustomer.phone_number)
                availableGram90Beans = Stock.objects.get(
                    package_type="90 grams - Beans")
                availableGram90Ground = Stock.objects.get(
                    package_type="90 grams - Ground")
                availableGram250Beans = Stock.objects.get(
                    package_type="250 grams - Beans")
                availableGram250Ground = Stock.objects.get(
                    package_type="250 grams - Ground")
                availableGram400Beans = Stock.objects.get(
                    package_type="400 grams - Beans")
                availableGram400Ground = Stock.objects.get(
                    package_type="400 grams - Ground")
                availableGram750Beans = Stock.objects.get(
                    package_type="750 grams - Beans")
                availableGram750Ground = Stock.objects.get(
                    package_type="750 grams - Ground")
                availableKg1Beans = Stock.objects.get(
                    package_type="1 kilogram - Beans")
                availableKg1Ground = Stock.objects.get(
                    package_type="1 kilogram - Ground")

                if (orderDetails.gram_90_beans > availableGram90Beans.total):
                    messages.warning(
                        request, 'The invoice can not be generated. Beacuse, 90 grams beans package is lower than in the order.')
                    return redirect('/createInvoice/'+pk)
                elif(orderDetails.gram_90_ground > availableGram90Ground.total):
                    messages.warning(
                        request, 'The invoice can not be generated. Beacuse, 90 grams ground package is lower than in the order.')
                    return redirect('/createInvoice/'+pk)
                elif(orderDetails.gram_250_beans > availableGram250Beans.total):
                    messages.warning(
                        request, 'The invoice can not be generated. Beacuse, 250 grams beans package is lower than in the order.')
                    return redirect('/createInvoice/'+pk)
                elif(orderDetails.gram_250_ground > availableGram250Ground.total):
                    messages.warning(
                        request, 'The invoice can not be generated. Beacuse, 250 grams ground package is lower than in the order.')
                    return redirect('/createInvoice/'+pk)
                elif(orderDetails.gram_400_beans > availableGram400Beans.total):
                    messages.warning(
                        request, 'The invoice can not be generated. Beacuse, 400 grams beans package is lower than in the order.')
                    return redirect('/createInvoice/'+pk)
                elif(orderDetails.gram_400_ground > availableGram400Ground.total):
                    messages.warning(
                        request, 'The invoice can not be generated. Beacuse, 400 grams ground package is lower than in the order.')
                    return redirect('/createInvoice/'+pk)
                elif(orderDetails.gram_750_beans > availableGram750Beans.total):
                    messages.warning(
                        request, 'The invoice can not be generated. Beacuse, 750 grams beans package is lower than in the order.')
                    return redirect('/createInvoice/'+pk)
                elif(orderDetails.gram_750_ground > availableGram750Ground.total):
                    messages.warning(
                        request, 'The invoice can not be generated. Beacuse, 750 grams ground package is lower than in the order.')
                    return redirect('/createInvoice/'+pk)
                elif(orderDetails.kilogram_1_beans > availableKg1Beans.total):
                    messages.warning(
                        request, 'The invoice can not be generated. Beacuse, 1 kilogram beans package is lower than in the order.')
                    return redirect('/createInvoice/'+pk)
                elif(orderDetails.kilogram_1_ground > availableKg1Ground.total):
                    messages.warning(
                        request, 'The invoice can not be generated. Beacuse, 1 kilogram ground package is lower than in the order.')
                    return redirect('/createInvoice/'+pk)
                else:
                    if (discount_type == "byRate"):
                        if(discount_rate > 10):
                            messages.warning(
                                request, 'Discount rate shoud not be greater than 10%')
                            return redirect('/createInvoice/'+pk)
                        discountValue = (Decimal(
                            discount_rate / 100)) * orderDetails.amount_tzs
                        discount_rate = discount_rate
                    elif(discount_type == "byValue"):
                        discount_rate = (Decimal(
                            discountValue * 100)) / orderDetails.amount_tzs
                        if(discount_rate > 10):
                            messages.warning(
                                request, 'Discount value exceed the discount rate of 10%. Please, lower the discount value')
                            return redirect('/createInvoice/'+pk)
                        discountValue = discountValue
                    else:
                        discount_rate = 0
                        discountValue = 0
                    createsPDF(orderDetails, doc_type, deni_due_date,
                               discountValue, discount_rate)
                    # =======================================EDIT ORDER STATUS
                    invoice_number = orderDetails.id
                    invoice_number_string = invoice_number

                    if(doc_type == 'Receipt'):
                        Orders.objects.filter(id=pk).update(
                            order_status='Completed',
                            payment_status='Paid',
                            updated_by=request.user.username
                        )
                      
                    else:
                        Orders.objects.filter(id=pk).update(
                            order_status='Invoice Generated',
                            payment_status='Not Paid',
                            updated_by=request.user.username
                        )

                        Invoice.objects.create(
                            invoice_number=invoice_number_string,
                            invoice_date=datetime.datetime.now().strftime("%d-%m-%Y"),
                            # customer info
                            customer_name=fetchCustomer.customer_name,
                            phone_number=fetchCustomer.phone_number,
                            email_address=fetchCustomer.email,
                            gram_90_beans=orderDetails.gram_90_beans,
                            gram_90_ground=orderDetails.gram_90_ground,
                            gram_250_beans=orderDetails.gram_250_beans,
                            gram_250_ground=orderDetails.gram_90_ground,
                            gram_400_beans=orderDetails.gram_400_beans,
                            gram_400_ground=orderDetails.gram_400_ground,
                            gram_750_beans=orderDetails.gram_750_beans,
                            gram_750_ground=orderDetails.gram_750_ground,
                            kilogram_1_beans=orderDetails.kilogram_1_beans,
                            kilogram_1_ground=orderDetails.kilogram_1_ground,
                            total_kg_beans=orderDetails.total_kg_beans,
                            total_kg_ground=orderDetails.total_kg_ground,
                            total_kgs=orderDetails.total_kgs,
                            # Invoice total
                            discount=discountValue,
                            discount_rate=discount_rate,

                            sub_total=orderDetails.amount_sub_total_tzs,
                            tax=orderDetails.amount_vat_tzs,
                            total=(orderDetails.amount_tzs - discountValue) +1,
                            document_type=doc_type,
                            payment_status='Not Paid',
                        )

                    # ======================================= UPDATE STOCK ===============================
                    ourProductGram90Beans = PackageList.objects.get(
                        package_name="90 grams - Beans")
                    ourProductGram90Ground = PackageList.objects.get(
                        package_name="90 grams - Ground")
                    ourProductGram250Beans = PackageList.objects.get(
                        package_name="250 grams - Beans")
                    ourProductGram250Ground = PackageList.objects.get(
                        package_name="250 grams - Ground")
                    ourProductGram400Beans = PackageList.objects.get(
                        package_name="400 grams - Beans")
                    ourProductGram400Ground = PackageList.objects.get(
                        package_name="400 grams - Ground")
                    ourProductGram750Beans = PackageList.objects.get(
                        package_name="750 grams - Beans")
                    ourProductGram750Ground = PackageList.objects.get(
                        package_name="750 grams - Ground")
                    ourProductKg1Beans = PackageList.objects.get(
                        package_name="1 kilogram - Beans")
                    ourProductKg1Ground = PackageList.objects.get(
                        package_name="1 kilogram - Ground")

                    Stock.objects.filter(package_type="90 grams - Beans").update(
                        total=(availableGram90Beans.total -
                               orderDetails.gram_90_beans),
                        total_kg=(availableGram90Beans.total_kg -
                                  (ourProductGram90Beans.package_weight * orderDetails.gram_90_beans)),
                        wholesale_total_price=((ourProductGram90Beans.wholesale_price) * (
                            availableGram90Beans.total - orderDetails.gram_90_beans)),
                        retail_total_price=((ourProductGram90Beans.retail_price) * (availableGram90Beans.total - orderDetails.gram_90_beans)))

                    Stock.objects.filter(package_type="90 grams - Ground").update(
                        total=(availableGram90Ground.total -
                               orderDetails.gram_90_ground),
                        total_kg=(availableGram90Ground.total_kg -
                                  (ourProductGram90Ground.package_weight * orderDetails.gram_90_ground)),
                        wholesale_total_price=((ourProductGram90Ground.wholesale_price) * (
                            availableGram90Ground.total - orderDetails.gram_90_ground)),
                        retail_total_price=((ourProductGram90Ground.retail_price) * (availableGram90Ground.total - orderDetails.gram_90_ground)))

                    Stock.objects.filter(package_type="250 grams - Beans").update(
                        total=(availableGram250Beans.total -
                               orderDetails.gram_250_beans),
                        total_kg=(availableGram250Beans.total_kg -
                                  (ourProductGram250Beans.package_weight * orderDetails.gram_250_beans)),
                        wholesale_total_price=(ourProductGram250Beans.wholesale_price * (
                            availableGram250Beans.total - orderDetails.gram_250_beans)),
                        retail_total_price=(ourProductGram250Beans.retail_price * (availableGram250Beans.total - orderDetails.gram_250_beans)))

                    Stock.objects.filter(package_type="250 grams - Ground").update(
                        total=(availableGram250Ground.total -
                               orderDetails.gram_250_ground),
                        total_kg=(availableGram250Ground.total_kg -
                                  (ourProductGram250Ground.package_weight * orderDetails.gram_250_ground)),
                        wholesale_total_price=(ourProductGram250Ground.wholesale_price * (
                            availableGram250Ground.total - orderDetails.gram_250_ground)),
                        retail_total_price=(ourProductGram250Ground.retail_price * (availableGram250Ground.total - orderDetails.gram_250_ground)))

                    Stock.objects.filter(package_type="400 grams - Beans").update(
                        total=(availableGram400Beans.total -
                               orderDetails.gram_400_beans),
                        total_kg=(availableGram400Beans.total_kg -
                                  (ourProductGram400Beans.package_weight * orderDetails.gram_400_beans)),
                        wholesale_total_price=(ourProductGram400Beans.wholesale_price * (
                            availableGram400Beans.total - orderDetails.gram_400_beans)),
                        retail_total_price=(ourProductGram400Beans.retail_price * (availableGram400Beans.total - orderDetails.gram_400_beans)))

                    Stock.objects.filter(package_type="400 grams - Ground").update(
                        total=(availableGram400Ground.total -
                               orderDetails.gram_400_ground),
                        total_kg=(availableGram400Ground.total_kg -
                                  (ourProductGram400Ground.package_weight * orderDetails.gram_400_ground)),
                        wholesale_total_price=(ourProductGram400Ground.wholesale_price * (
                            availableGram400Ground.total - orderDetails.gram_400_ground)),
                        retail_total_price=(ourProductGram400Ground.retail_price * (availableGram400Ground.total - orderDetails.gram_400_ground)))

                    Stock.objects.filter(package_type="750 grams - Beans").update(
                        total=(availableGram750Beans.total -
                               orderDetails.gram_750_beans),
                        total_kg=(availableGram750Beans.total_kg -
                                  (ourProductGram750Beans.package_weight * orderDetails.gram_750_beans)),
                        wholesale_total_price=(ourProductGram750Beans.wholesale_price * (
                            availableGram750Beans.total - orderDetails.gram_750_beans)),
                        retail_total_price=(ourProductGram750Beans.retail_price * (availableGram750Beans.total - orderDetails.gram_750_beans)))

                    Stock.objects.filter(package_type="750 grams - Ground").update(
                        total=(availableGram750Ground.total -
                               orderDetails.gram_750_ground),
                        total_kg=(availableGram750Ground.total_kg -
                                  (ourProductGram750Ground.package_weight * orderDetails.gram_750_ground)),
                        wholesale_total_price=(ourProductGram750Ground.wholesale_price * (
                            availableGram750Ground.total - orderDetails.gram_750_ground)),
                        retail_total_price=(ourProductGram750Ground.retail_price * (availableGram750Ground.total - orderDetails.gram_750_ground)))

                    Stock.objects.filter(package_type="1 kilogram - Beans").update(
                        total=(availableKg1Beans.total -
                               orderDetails.kilogram_1_beans),
                        total_kg=(availableKg1Beans.total_kg -
                                  (ourProductKg1Beans.package_weight * orderDetails.kilogram_1_beans)),
                        wholesale_total_price=(ourProductKg1Beans.wholesale_price * (
                            availableKg1Beans.total - orderDetails.kilogram_1_beans)),
                        retail_total_price=(ourProductKg1Beans.retail_price * (availableKg1Beans.total - orderDetails.kilogram_1_beans)))

                    Stock.objects.filter(package_type="1 kilogram - Ground").update(
                        total=(availableKg1Ground.total -
                               orderDetails.kilogram_1_ground),
                        total_kg=(availableKg1Ground.total_kg -
                                  (ourProductKg1Ground.package_weight * orderDetails.kilogram_1_ground)),
                        wholesale_total_price=(ourProductKg1Ground.wholesale_price * (
                            availableKg1Ground.total - orderDetails.kilogram_1_ground)),
                        retail_total_price=(ourProductKg1Ground.retail_price * (availableKg1Ground.total - orderDetails.kilogram_1_ground)))

                    # =========IF THE CUSTOMER MAKE AN ORDER FOR THE FIRST TIME THIS WILL MAKE HIM/HER VISIBLE AS OUR CUSTOMER
                    if(fetchCustomer.visible == 0):
                        Customer.objects.filter(
                            user_id=orderDetails.customer_id).update(visible=1)
                    # ======AFTER GENERATIONG INVOICE ADD ORDER INFO TO MADENI
                    try:
                        # Madeni.objects.filter(customer_id=customer.id).exists():
                        fetchDeni = Madeni.objects.get(
                            customer_id=orderDetails.customer_id)
                        total_deni_tzs = fetchDeni.deni_amount_tzs + (orderDetails.amount_tzs - discountValue)
                        total_deni_usd = fetchDeni.deni_amount_usd + orderDetails.amount_usd
                        deni_due_date = deni_due_date
                        Madeni.objects.filter(customer_id=orderDetails.customer_id).update(deni_amount_tzs=total_deni_tzs,
                                                                                           deni_amount_usd=total_deni_usd, deni_due_date=deni_due_date, served_by=request.user.username,)
                    except Madeni.DoesNotExist:
                        total_deni_tzs = orderDetails.amount_tzs
                        total_deni_usd = orderDetails.amount_usd
                        Madeni.objects.create(
                            customer_id=orderDetails.customer_id,
                            deni_amount_tzs=(total_deni_tzs - discountValue),
                            deni_amount_usd=total_deni_usd,
                            deni_due_date=deni_due_date,
                            served_by=request.user.username)

            except Customer.DoesNotExist:
                messages.warning(
                    request, 'Please check if the customer is in our customer list.')
                return redirect('/orderDetails/'+pk)
            return redirect('/orders/')

    else:
        form = InvoiceForm(request.POST)
        form = InvoiceForm(use_required_attribute=False)
    context = {
        'title': "Discount info",
        'form': form
    }
    return render(request, 'staff/add_invoice.html', context)


# INVOICE DETAILS INVOICE
@login_required
def invoice_details(request, id):
    company_info = CompanyInfo.objects.get()
    if request.user.is_staff != 1:
        return HttpResponseNotFound("<h1>Error 404: Access to this page is restricted<h1>")
    invoiceDetails = Invoice.objects.get(pk=id)
    userdetails = get_object_or_404(User, email=invoiceDetails.email_address)
    try:
        customer_ordered = Customer.objects.get(email=userdetails.email)
    except Customer.DoesNotExist:
        customer_ordered = 'staff'

    totalpaid = 0
    try:
        paymentInfo = Payments.objects.filter(order_number=invoiceDetails.invoice_number)
        for paidAmount in paymentInfo:
            totalpaid = totalpaid + paidAmount.paid_amount_tzs
    except Payments.DoesNotExist:
        totalpaid = 0.00

    allPayments = Payments.objects.filter(order_number=invoiceDetails.invoice_number)
    context = {
        'company_info': company_info,
        'invoiceDetails': invoiceDetails,
        'allPayments': allPayments,
        'totalPaid': totalpaid,
        'customer_ordered': customer_ordered,
        'title': 'Invoice Details',
    }

    return render(request, 'staff/invoice_details.html', context)


@login_required
def availabe_stocks(request):
    if request.user.is_staff != 1:
        return HttpResponseNotFound("<h1>Error 404: Access to this page is restricted<h1>")
    our_product = PackageList.objects.all()
    title = "Stocks Available"
    queryset = Stock.objects.all()

    context = {
        'title': title,
        'queryset': queryset,
        'our_product': our_product,
        'sumData': find_total()
    }
    return render(request, 'staff/available_stock.html', context)


@login_required
def availabe_stocks_update(request, pk):
    if request.user.is_staff != 1:
        return HttpResponseNotFound("<h1>Error 404: Access to this page is restricted<h1>")
    old_stock = Stock.objects.get(id=pk)  # select data based on primary key
    previous_stock = old_stock.new_stock
    previous_stock_date = old_stock.new_stock_date
    package_type = old_stock.package_type
    total_pcs_old = old_stock.total
    queryset = Stock.objects.all()

    our_product = PackageList.objects.get(package_name=package_type)
    form = StockUpdateForm(instance=old_stock)

    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=old_stock)
        if form.is_valid():

            new_stock = form.cleaned_data['new_stock']
            total_pcs = new_stock + total_pcs_old
            wholesale_total_price = (our_product.wholesale_price * total_pcs)
            retail_total_price = (our_product.retail_price * total_pcs)
            package_weight = our_product.package_weight * total_pcs

            Stock.objects.filter(package_type=package_type).update(
                new_stock=new_stock,
                previous_stock=previous_stock,
                previous_stock_date=previous_stock_date,
                total=total_pcs,
                total_kg=package_weight,
                wholesale_total_price=wholesale_total_price,
                retail_total_price=retail_total_price
            )

            return redirect('/availabe_stocks/')
    context = {
        'buttonTitle': 'Update',
        'form': form,
        'old_stock': old_stock,
        'queryset': queryset,
        'our_product': our_product
    }
    return render(request, 'staff/available_stock.html', context)


@login_required
def customers(request):
    if request.user.is_staff != 1:
        return HttpResponseNotFound("<h1>Error 404: Access to this page is restricted<h1>")
    title = "customers"
    customer = Customer.objects.filter(visible=1)
    myFilter = CustomersFilters(request.GET, queryset=customer)
    customer = myFilter.qs
    context = {
        'customer': customer,
        'title': title,
        'myFilter': myFilter,
    }

    return render(request, 'staff/customer.html', context)


@login_required
def farmers(request):
    if request.user.is_staff != 1:
        return HttpResponseNotFound("<h1>Error 404: Access to this page is restricted<h1>")
    title = "Farmers"
    farmers = Farmers.objects.all()
    myFilter = WakulimaFilters(request.GET, queryset=farmers)
    farmers = myFilter.qs
    context = {
        'farmers': farmers,
        'title': title,
        'myFilter': myFilter,
    }
    return render(request, 'staff/farmers.html', context)


@login_required
def farmerDetails(request, id):
    company_info = CompanyInfo.objects.get()
    farmerDetails = get_object_or_404(Farmers, pk=id)
    taarifaZashamba = TaarifaZaShamba.objects.filter(mkulima=id)
    geolocator = Nominatim(user_agent="invoicemgmt")
    location = geolocator.geocode(farmerDetails.kijiji)
    if (location == None):
        address_Latlng = [-9.933070660065649, 35.53557376441188]
    else:
        address_Latlng = [location.latitude, location.longitude]
    m = folium.Map(location=address_Latlng, zoom_start=5)
    # add marker to map
    folium.Marker(address_Latlng, popup='INFO',
                  tooltip=farmerDetails.kijiji,
                  icon=folium.Icon(color="red", icon="info-sign"),

                  ).add_to(m)
    m = m._repr_html_()

    context = {
        'company_info': company_info,
        'farmerDetails': farmerDetails,
        'shamba': taarifaZashamba,
        'm': m,
        'title': 'Farmer Details',
    }
    return render(request, 'staff/farmer_details.html', context)


@login_required
def updateFarmer(request, id):
    if request.user.is_staff != 1:
        return HttpResponseNotFound("<h1>Error 404: Access to this page is restricted<h1>")
    company_info = CompanyInfo.objects.get()
    farmerDetails = get_object_or_404(Farmers, pk=id)

    form = UpdateFarmerForm()
    if request.method == 'POST':
        form = UpdateFarmerForm(request.POST)
        if form.is_valid():

            kuandaa_shamba = form.cleaned_data['kuandaa_shamba']
            kupanda = form.cleaned_data['kupanda']
            hari_ya_shamba = form.cleaned_data['hari_ya_shamba']
            hari_ya_hewa = form.cleaned_data['hari_ya_hewa']
            mabadiriko = form.cleaned_data['mabadiriko']
            mavuno = form.cleaned_data['mavuno']
            maoni = form.cleaned_data['maoni']

            TaarifaZaShamba.objects.create(
                mkulima=id,
                kuandaa_shamba=kuandaa_shamba,
                kupanda=kupanda,
                hari_ya_shamba=hari_ya_shamba,
                hari_ya_hewa=hari_ya_hewa,
                mabadiriko=mabadiriko,
                mavuno=mavuno,
                maoni=maoni,)

            messages.success(
                request, 'Hongera, Umefanikiwa kuhifadhi taarifa za shamba.')
            return redirect('/farmerDetails/'+str(id))

    context = {
        'company_info': company_info,
        'form': form,
        'farmerDetails': farmerDetails,
        'title': 'Jaza Taarifa Za Shamba',
        # 'customer_ordered': customer_ordered,
    }

    return render(request, 'staff/farmer_taarifa.html', context)


@login_required
def add_customer(request):
    if request.user.is_staff != 1:
        return HttpResponseNotFound("<h1>Error 404: Access to this page is restricted<h1>")
    title = "Add New Customer"
    if request.method == 'POST':
        form = AddCustomerForm(request.POST)
        if form.is_valid():
            customer_name = form.cleaned_data['customer_name']
            username = form.cleaned_data['username']
            email = email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            postal_address = form.cleaned_data['postal_address']

            if User.objects.filter(username=username).exists():
                messages.error(request, 'The username already exists.')
            elif Customer.objects.filter(phone_number=phone_number).exists():
                messages.error(request, 'The phone number already exists.')
            else:
                # SAVE USER INTO TABLE USER
                password = make_password(email)
                user = User.objects.create(
                    username=username,
                    password=password,
                    email=email,
                    date_joined=datetime.datetime.now(),
                )
                # SAVE USER INTO TABLE CUSTOMER
                customer = Customer.objects.create(
                    customer_name=customer_name,
                    postal_address=postal_address,
                    email=email,
                    phone_number=phone_number,
                    user_id=user.id,
                    visible=0,
                    added_by=request.user.username
                )
                messages.success(
                    request, 'Successfull added new customer.')
        else:
            print(form.errors)
    else:
        form = AddCustomerForm(request.POST)
        form = AddCustomerForm(use_required_attribute=False)
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'staff/add_customer.html', context)



@login_required
def orders(request):
    if request.user.is_staff != 1:
        return HttpResponseNotFound("<h1>Error 404: Access to this page is restricted<h1>")
    title = "Orders"
    order = Orders.objects.order_by('-order_date').all()
    myFilter = OrderFilters(request.GET, queryset=order)
    order = myFilter.qs

    totalpaid = 0
    total = 0
    dat = []

    for allOders in order:
        paymentInfo = Payments.objects.filter(order_number=allOders.id)
        for paidAmount in paymentInfo:
            total = total + paidAmount.paid_amount_tzs 
        totalpaid = total
        dat.append(totalpaid)
        total = 0 
     
    context = {
        'order': order,
        'title': title,
        'myFilter': myFilter,
        'totalpaid':dat
    }
        
    return render(request, 'staff/order.html', context)


@login_required
def orderDetails(request, id):
    company_info = CompanyInfo.objects.get()
    orderDetails = get_object_or_404(Orders, pk=id)
    userdetails = get_object_or_404(User, username=orderDetails.customer)
    try:
        customer_ordered = Customer.objects.get(email=userdetails.email)
    except Customer.DoesNotExist:
        customer_ordered = 'staff'

    totalpaid = 0
    try:
        paymentInfo = Payments.objects.filter(order_number=id)
        for paidAmount in paymentInfo:
            totalpaid = totalpaid + paidAmount.paid_amount_tzs
    except Payments.DoesNotExist:
        totalpaid = 0.00

    

    context = {
        'company_info': company_info,
        'orderDetails': orderDetails,
        'totalpaid' : totalpaid,
        'customer_ordered': customer_ordered,
        'title': 'Orders Details',
    }
    return render(request, 'staff/order_details.html', context)


@login_required
def new_orders(request):
    title = "Orders"
    order = Orders.objects.filter(order_status__contains='New')
    context = {
        'order': order,
        'title': title,
    }
    return render(request, 'staff/order.html', context)


@login_required
def pending_orders(request):
    title = "Pending Orders"
    order = Orders.objects.filter(order_status__contains='Pending')
    context = {
        'order': order,
        'title': title,
    }
    return render(request, 'staff/order.html', context)


def find_total_madeni():
    queryset = Madeni.objects.all()

    # Calculating sum of madeni
    sumData = object()
    sum_of_tzs = 0
    sum_of_usd = 0

    for dat in queryset:

        sum_of_tzs = sum_of_tzs + dat.deni_amount_tzs
        sum_of_usd = sum_of_usd + dat.deni_amount_usd
        sumData = {
            'sum_of_tzs': locale.format("%d", sum_of_tzs, grouping=True),
            'sum_of_usd': sum_of_usd
        }
    return sumData


@login_required
def madeni(request):
    if request.user.is_staff != 1:
        return HttpResponseNotFound("<h1>Error 404: Access to this page is restricted<h1>")

    madeni = Madeni.objects.order_by('-created_at').all()
    myFilter = MadeniFilters(request.GET, queryset=madeni)
    madeni = myFilter.qs

    context = {
        'madeni': madeni,
        'title': 'Madeni',
        'myFilter': myFilter,
        'totat_deni': find_total_madeni()
    }
    return render(request, 'staff/madeni.html', context)


@login_required
def add_deni(request):
    if request.user.is_staff != 1:
        return HttpResponseNotFound("<h1>Error 404: Access to this page is restricted<h1>")
    title = "Add New Debt"
    if request.method == 'POST':
        form = MadeniForm(request.POST)
        if form.is_valid():
            customer = form.cleaned_data['customer']
            deni_amount_tzs = form.cleaned_data['deni_amount_tzs']
            deni_amount_usd = form.cleaned_data['deni_amount_usd']
            deni_due_date = form.cleaned_data['deni_due_date']
            try:
                # Madeni.objects.filter(customer_id=customer.id).exists():
                fetchDeni = Madeni.objects.get(customer_id=customer.id)
                total_deni_tzs = fetchDeni.deni_amount_tzs + deni_amount_tzs
                total_deni_usd = fetchDeni.deni_amount_usd + deni_amount_usd
                deni_due_date = deni_due_date
                Madeni.objects.filter(customer_id=customer.id).update(deni_amount_tzs=total_deni_tzs,
                                                                      deni_amount_usd=total_deni_usd, deni_due_date=deni_due_date, served_by=request.user.username,)

            except Madeni.DoesNotExist:
                total_deni_tzs = deni_amount_tzs
                total_deni_usd = deni_amount_usd
                Madeni.objects.create(
                    customer=customer,
                    deni_amount_tzs=total_deni_tzs,
                    deni_amount_usd=total_deni_usd,
                    deni_due_date=deni_due_date,
                    served_by=request.user.username)

            messages.success(
                request, 'Successfull added new dept.')
            return redirect('/madeni/')
        else:
            print(form.errors)
    else:
        form = MadeniForm(request.POST)
        form = MadeniForm(use_required_attribute=False)
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'staff/add_deni.html', context)


def find_total_paid():
    queryset = Payments.objects.all()

    # Calculating sum of madeni
    sumData = object()
    sum_of_tzs = 0
    sum_of_usd = 0

    for dat in queryset:
        sum_of_tzs = sum_of_tzs + dat.deni_amount_tzs
        sum_of_usd = sum_of_usd + dat.deni_amount_usd
        sumData = {
            'sum_of_tzs': locale.format("%d", sum_of_tzs, grouping=True),
            'sum_of_usd': sum_of_usd
        }
    return sumData


@login_required
def payments(request):
    if request.user.is_staff != 1:
        return HttpResponseNotFound("<h1>Error 404: Access to this page is restricted<h1>")
    if request.method == 'POST':
        customer = request.POST.get('customer')
        fromDate = request.POST.get('fromDate')
        toDate = request.POST.get('toDate')

        searchResults = Payments.objects.raw(
            'select * from invoicemgmt_payments where payment_date between "'+fromDate+'" and "'+toDate+'"')

        context = {
            'payments': searchResults,
            'title': 'Payments',
            # 'myFilter': myFilter,
        }
        return render(request, 'staff/payments.html', context)
    else:
        payments = Payments.objects.order_by('-payment_date').all()
        # myFilter = PaymentsFilters(request.GET, queryset=payments)
        # payments = myFilter.qs

        context = {
            'payments': payments,
            'title': 'Payments',
            # 'myFilter': myFilter,
        }
        return render(request, 'staff/payments.html', context)

def find_total_expenses():
    queryset = Expenses.objects.all()

    # Calculating sum of madeni
    sumData = object()
    sum_of_tzs = 0

    for dat in queryset:

        sum_of_tzs = sum_of_tzs + dat.paid_amount
        sumData = {
            'sum_of_tzs': locale.format("%d", sum_of_tzs, grouping=True),
        }
    return sumData

@login_required
def expenses(request):
    if request.user.is_staff != 1:
        return HttpResponseNotFound("<h1>Error 404: Access to this page is restricted<h1>")
    if request.method == 'POST':
        fromDate = request.POST.get('fromDate')
        toDate = request.POST.get('toDate')

        searchResults = Expenses.objects.raw(
            'select * from invoicemgmt_expenses where payment_date between "'+fromDate+'" and "'+toDate+'"')

        sum_of_tzs = 0
        sumData = object()
        sumData = {
                'sum_of_tzs': 0,
            }
        for paid in searchResults:
            sum_of_tzs = sum_of_tzs + paid.paid_amount
            sumData = {
                'sum_of_tzs': locale.format("%d", sum_of_tzs, grouping=True),
            }

        context = {
            'payments': searchResults,
            'title': 'Expenses',
            'totat_expense': sumData
            # 'myFilter': myFilter,
        }
        return render(request, 'staff/expenses.html', context)
    else:
        payments = Expenses.objects.order_by('-payment_date').all()
        # myFilter = PaymentsFilters(request.GET, queryset=payments)
        # payments = myFilter.qs

        context = {
            'payments': payments,
            'title': 'Expenses',
            'totat_expense': find_total_expenses()

            # 'myFilter': myFilter,
        }
        return render(request, 'staff/expenses.html', context)


@login_required
def add_payment(request, id):
    if request.user.is_staff != 1:
        return HttpResponseNotFound("<h1>Error 404: Access to this page is restricted<h1>")

    orderDetails = get_object_or_404(Orders, pk=id)
    userdetails = get_object_or_404(User, username=orderDetails.customer)
    customer_ordered = Customer.objects.get(user_id=userdetails.id)

    title = "Upload Proof of Payment"
    if request.method == 'POST':
        form = PaymentsForm(request.POST, request.FILES)
        if form.is_valid():
            amount_paid = form.cleaned_data['paid_amount_tzs']
            proof_of_payment = request.FILES.get('proof_of_payment', False)
            fetchDeni = Madeni.objects.get(
                customer_id=customer_ordered.user_id)
            
            if(amount_paid < 1):
                messages.error(
                request, 'Payments Should be not less than 0.')
                return redirect('/add_payment/'+str(id))

            Payments.objects.create(
                customer=userdetails,
                paid_amount_tzs=amount_paid,
                order_number=id,
                proof_of_payment=proof_of_payment,
                updated_by=request.user.username)
            
            paymentInfo = Payments.objects.filter(order_number=id)
            discountInfo = Invoice.objects.get(invoice_number=id)

            totalpaid = 0
            for paidAmount in paymentInfo:
                totalpaid = totalpaid + paidAmount.paid_amount_tzs

            if (totalpaid < discountInfo.total):
                Orders.objects.filter(id=id).update(
                    order_status='Paid Some',
                    payment_status='Paid Some',
                    updated_by=request.user.username
                )
                Invoice.objects.filter(invoice_number=id).update(
                    payment_status='Paid Some'
                )
            else:
                Orders.objects.filter(id=id).update(
                    order_status='Paid',
                    payment_status='Paid',
                    order_completion_date = datetime.datetime.now().strftime("%Y-%m-%d"),
                    updated_by=request.user.username
                )
                Invoice.objects.filter(invoice_number=id).update(
                    payment_status='Paid'
                )

            # update table madeni baada ya mteja kulipa
            balance_deni_tzs = fetchDeni.deni_amount_tzs - amount_paid
            # balance_deni_usd = fetchDeni.deni_amount_usd - orderDetails.amount_usd

            if (balance_deni_tzs <= 0):
                Madeni.objects.get(
                    customer_id=customer_ordered.user_id).delete()
            else:
                Madeni.objects.filter(customer_id=customer_ordered.user_id).update(deni_amount_tzs=balance_deni_tzs)

            messages.success(
                request, 'Successfull added new payment.')
            return redirect('/payments/')
        else:
            print(form.errors)
    else:
        form = PaymentsForm(request.POST)
        form = PaymentsForm(use_required_attribute=False)
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'staff/add_payment.html', context)

@login_required
def add_expenses(request):
    if request.user.is_staff != 1:
        return HttpResponseNotFound("<h1>Error 404: Access to this page is restricted<h1>")

    title = "Upload Expenses Information"
    if request.method == 'POST':
        form = ExpensesForm(request.POST, request.FILES)
        if form.is_valid():
            payee = form.cleaned_data['payee']
            description = form.cleaned_data['description']
            amount_paid = form.cleaned_data['paid_amount']
            proof_of_payment = request.FILES.get('proof_of_payment', False)

            Expenses.objects.create(
                payee=payee,
                description = description,
                paid_amount=amount_paid,
                payment_date = datetime.datetime.now(),
                proof_of_payment=proof_of_payment,
                updated_by=request.user.username)
            
            messages.success(
                request, 'Successfull added new debt.')
            return redirect('/expenses/')
        else:
            print(form.errors)
    else:
        form = ExpensesForm(request.POST)
        form = ExpensesForm(use_required_attribute=False)
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'staff/add_expenses.html', context)


def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type='aplication/proofs')
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(file_path)
            return response
    raise Http404


@login_required
def stocks_out(request):
    if request.user.is_staff != 1:
        return HttpResponseNotFound("<h1>Error 404: Access to this page is restricted<h1>")
    title = "Stocks Available"
    context = {
        'title': title,
    }
    return render(request, 'staff/stock_out.html', context)

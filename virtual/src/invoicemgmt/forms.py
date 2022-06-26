from datetime import date
from django.contrib.auth.models import User
from django import forms
# from .models import *
from .models import *



class DateInput(forms.DateInput):
    input_type = 'date'


class CustomerRegisterForm(forms.ModelForm):
    customer_name = forms.CharField(label=(u'Customer Name'))
    username = forms.CharField(label=(u'Username'))
    email = forms.EmailField(label=(u'Email Address'))
    phone_number = forms.CharField(label=('Phone Number'))
    postal_address = forms.CharField(label=('Address'))
    password = forms.CharField(
        label=(u'Password'), widget=forms.PasswordInput(render_value=False))
    password1 = forms.CharField(
        label=(u'Verify Password'), widget=forms.PasswordInput(render_value=False))
    visible = forms.IntegerField(required=False)
    user = forms.IntegerField(required=False)

    class Meta:
        model = Customer
        fields = "__all__"

    def clean_customer_name(self):
        customer_name = self.cleaned_data.get('customer_name')
        if not customer_name:
            raise forms.ValidationError('')
        return customer_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number:
            raise forms.ValidationError('')
        return phone_number

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('')
        return email


class AddCustomerForm(forms.ModelForm):
    customer_name = forms.CharField(label=(u'Customer Name'))
    username = forms.CharField(label=(u'Username'))
    email = forms.EmailField(label=(u'Email Address'))
    phone_number = forms.CharField(label=('Phone Number'))
    postal_address = forms.CharField(label=('Address'))
    visible = forms.IntegerField(required=False)
    user = forms.IntegerField(required=False)
    class Meta:
        model = Customer
        fields = "__all__"
# ['kuandaa_shamba', 'kupanda', 'hari_ya_shamba', 'hari_ya_hewa', 'mabadiriko', 'mavuno',
#                   'maoni']

class UpdateFarmerForm(forms.ModelForm):
    kuandaa_shamba = forms.DateField(widget=DateInput)
    kupanda = forms.DateField(widget=DateInput)
    class Meta:
        model = TaarifaZaShamba
        fields = "__all__"


# class InvoiceForm(forms.ModelForm):
#     generate_invoice = forms.BooleanField(required=False)
#     class Meta:
#         model = Invoice
#         fields = ['invoice_number', 'invoice_date', 'customer_name', 'post_address', 'phone_number', 'email_address',
#                   'product_name1', 'product_quantity1', 'product_price1', 'product_total_price1',
#                   'product_name2', 'product_quantity2', 'product_price2', 'product_total_price2',
#                   'product_name3', 'product_quantity3', 'product_price3', 'product_total_price3',
#                   'product_name4', 'product_quantity4', 'product_price4', 'product_total_price4',
#                   'product_name5', 'product_quantity5', 'product_price5', 'product_total_price5',
#                   'product_name6', 'product_quantity6', 'product_price6', 'product_total_price6',
#                   'product_name7', 'product_quantity7', 'product_price7', 'product_total_price7',
#                   'product_name8', 'product_quantity8', 'product_price8', 'product_total_price8',
#                   'sub_total', 'tax', 'discount_rate', 'discount', 'total', 'paid', 'document_type', 'generate_invoice']

#     def clean_customer_name(self):
#         customer_name = self.cleaned_data.get('customer_name')
#         if not customer_name:
#             raise forms.ValidationError('')
#         return customer_name

#     def clean_phone_number(self):
#         phone_number = self.cleaned_data.get('phone_number')
#         if not phone_number:
#             raise forms.ValidationError('')
#         return phone_number

#     def clean_product_name1(self):
#         product_name1 = self.cleaned_data.get('product_name1')
#         print("product_name1"+product_name1)
#         if product_name1 == 0:
#             raise forms.ValidationError('')
#         return product_name1

#     def clean_product_quantity1(self):
#         product_quantity1 = self.cleaned_data.get('product_quantity1')
#         if not product_quantity1:
#             raise forms.ValidationError('')
#         return product_quantity1


class InvoiceForm(forms.ModelForm):
    
    CHOICES = [('byRate','By Rate'),('byValue','By Value')]
    discount_type=forms.CharField(label='Discount Type', widget=forms.RadioSelect(choices=CHOICES), required=False)
    class Meta:
        model = Invoice
        fields = ['discount_type','discount_rate', 'discount']

    def clean_discount_rate(self):
        discount_type = self.cleaned_data.get('discount_type')
        discount_rate = self.cleaned_data.get('discount_rate')
        if discount_type == "byRate"  and discount_rate < 0:
            raise forms.ValidationError('Please enter value for discount rate')
        return discount_rate

    def clean_discount(self):
        discount_type = self.cleaned_data.get('discount_type')
        discount_value = self.cleaned_data.get('discount')
        if discount_type == "byValue"  and discount_value < 0:
            raise forms.ValidationError('Please enter value for discount Value')
        return discount_value


class StockUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StockUpdateForm, self).__init__(*args, **kwargs)
        self.fields['package_type'].disabled = True

    class Meta:
        model = Stock
        fields = ['package_type', 'new_stock', 'previous_stock',
                  'previous_stock_date', 'total', 'total_kg', 'retail_total_price', 'wholesale_total_price']


# CUSTOMERS
class OrderNowForm(forms.ModelForm):
    gram_90_beans = forms.IntegerField(label=(u''), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'id': 'beans_90g'}), required=False)
    gram_90_ground = forms.IntegerField(label=(u''), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'id': 'ground_90g'}), required=False)
    gram_250_beans = forms.IntegerField(label=(u''), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'id': 'beans_250g'}), required=False)
    gram_250_ground = forms.IntegerField(label=(u''), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'id': 'ground_250g'}), required=False)
    gram_400_beans = forms.IntegerField(label=(u''), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'id': 'beans_400g'}), required=False)
    gram_400_ground = forms.IntegerField(label=(u''), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'id': 'ground_400g'}), required=False)
    gram_750_beans = forms.IntegerField(label=(u''), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'id': 'beans_750g'}), required=False)
    gram_750_ground = forms.IntegerField(label=(u''), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'id': 'ground_750g'}), required=False)
    kilogram_1_beans = forms.IntegerField(label=(u''), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'id': 'beans_1kg'}), required=False)
    kilogram_1_ground = forms.IntegerField(label=(u''), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'id': 'ground_1kg'}), required=False)
    total_kg_beans = forms.DecimalField(label=(u''), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'id': 'beans_total'}), required=False, disabled=True)
    total_kg_ground = forms.DecimalField(label=(u''), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'id': 'ground_total'}), required=False, disabled=True)
    total_kgs = forms.DecimalField(label=(u''),  widget=forms.TextInput( 
        attrs={'class': 'form-control form-control-sm', 'id': 'total_kgs', 'name':"total_kgs"}), required=False, disabled=True)
    amount_tzs = forms.DecimalField(label=(u''), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'id': 'total_amount_tzs'}), required=False, disabled=True)
    amount_usd = forms.DecimalField(label=(u''), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'id': 'total_amount_usd'}), required=False, disabled=True)
    amount_vat_tzs = forms.DecimalField(label=(u''), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'id': 'amount_vat_tzs'}), required=False, disabled=True)
    amount_vat_usd = forms.DecimalField(label=(u''), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'id': 'amount_vat_usd'}), required=False, disabled=True)
    amount_sub_total_tzs = forms.DecimalField(label=(u''), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'id': 'amount_sub_total_tzs'}), required=False, disabled=True)
    amount_sub_total_usd = forms.DecimalField(label=(u''), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'id': 'amount_sub_total_usd'}), required=False, disabled=True)

    class Meta:
        model = Orders
        fields = ['gram_90_beans', 'gram_90_ground', 'gram_250_beans', 'gram_250_ground', 'gram_400_beans', 'gram_400_ground',
                  'gram_750_beans', 'gram_750_ground', 'kilogram_1_beans', 'kilogram_1_ground', 'total_kg_beans', 'total_kg_ground',
                  'total_kgs', 'amount_sub_total_tzs', 'amount_sub_total_usd', 'amount_vat_tzs', 'amount_vat_usd', 'amount_tzs', 'amount_usd', 'order_status']


class CareerApply(forms.ModelForm):
    class Meta:
        model = JobApplications
        fields = "__all__"



class MadeniForm(forms.ModelForm):
    deni_due_date = forms.DateField(widget=DateInput)
    class Meta:
        model = Madeni
        fields = ['customer', 'deni_amount_tzs',
                  'deni_amount_usd', 'deni_due_date']

class PaymentsForm(forms.ModelForm):
    proof_of_payment = forms.FileField(required=True)
    error_css_class = "error"
    class Meta:
        model = Payments
        fields = ['paid_amount_tzs','proof_of_payment']


class ExpensesForm(forms.ModelForm):
    payee = forms.CharField(label=(u'Mlipwaji'),required=True)
    # description = forms.CharField(label=(u'Description'),required=True,max_length=4)
    paid_amount = forms.CharField(label=(u'Kiasi cha malipo'),required=True)
    proof_of_payment = forms.FileField(label=(u'Uthibitisha'),required=True)
    error_css_class = "error"
    class Meta:
        model = Expenses
        fields = ['payee','description','paid_amount','proof_of_payment']


class MkulimaForm(forms.ModelForm):
    class Meta:
        model = Farmers
        fields = "__all__"

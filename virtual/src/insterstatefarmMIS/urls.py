"""insterstatefarmMIS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.static import serve
from invoicemgmt.views import websiteViews, staffViews, customerViews


urlpatterns = [
    # Authentications
    path('register/', staffViews.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='auth/password_reset.html'), name='password_reset'),
    path('password-reset_done/',auth_views.PasswordResetDoneView.as_view(
        template_name='auth/password_reset_done.html'), name='password_reset_done'
         ),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
        template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'
         ),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


    # ADMIN
    path('admin/', admin.site.urls),

    # WEBSITE
    path('', websiteViews.website_home, name='website_home'),
    path('services', websiteViews.services, name='services'),
    path('news', websiteViews.news, name='news'),
    path('team', websiteViews.team, name='team'),
    path('add_farmers', websiteViews.add_farmers, name='add_farmers'),
    # careers
    path('careers', websiteViews.careers, name='careers'),
    path('<int:id>', websiteViews.careersDetails, name='careersDetails'),
    path('careersApply/<int:id>', websiteViews.careersApply, name='careersApply'),
    path('contact-us', websiteViews.contact_us, name='contact_us'),
    path('about-us', websiteViews.about_us, name='about_us'),

    # STAFFS
    path('s_dashboard/', staffViews.dashboard, name='dashboard'),
    # path('add_invoice/', staffViews.add_invoice, name='add_invoice'),
    path('all_invoices/', staffViews.all_invoices, name='all_invoices'),
    # path('update_invoice/<str:pk>',
    #      staffViews.update_invoice, name='update_invoice'),
    path('invoice_details/<int:id>',
         staffViews.invoice_details, name='invoice_details'),
    path('availabe_stocks/', staffViews.availabe_stocks, name='availabe_stocks'),
    path('stocks_out/', staffViews.stocks_out, name='stocks_out'),
    path('availabe_stocks_update/<str:pk>',
         staffViews.availabe_stocks_update, name='availabe_stocks_update'),
    path('orders/', staffViews.orders, name='orders'),
    path('orderDetails/<int:id>', staffViews.orderDetails, name='orderDetails'),
    path('createInvoice/<str:pk>', staffViews.createInvoice, name='createInvoice'),
    
    path('new_orders/', staffViews.orders, name='new_orders'),
    path('pending_orders/', staffViews.orders, name='pending_orders'),
    path('customers/', staffViews.customers, name='customers'),
    path('add_customer/', staffViews.add_customer, name='add_customer'),
    path('farmers/', staffViews.farmers, name='farmers'),
    path('farmerDetails/<int:id>', staffViews.farmerDetails, name='farmerDetails'),
    path('updateFarmer/<int:id>', staffViews.updateFarmer, name='updateFarmer'),
    path('madeni/', staffViews.madeni, name='madeni'),
    path('add_deni/', staffViews.add_deni, name='add_deni'),
    path('payments/', staffViews.payments, name='payments'),
    path('expenses/', staffViews.expenses, name='expenses'),
    path('add_payment/<int:id>', staffViews.add_payment, name='add_payment'),
    path('add_expenses/', staffViews.add_expenses, name='add_expenses'),
    url(r'^download/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
    



    # CUSTOMERS
    path('order_now/', customerViews.orderNow, name='order_now'),
    path('my_order/', customerViews.myOrders, name='my_order'),
    path('c_orderDetails/<int:id>', customerViews.orderDetails, name='c_orderDetails'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

from django.urls import path
from . import views
from .views import *


app_name = "payrollpayment"

urlpatterns = [
    # views for payment

    path('payroll_registration/', views.payroll_reg, name='payroll_reg'),
    path('payitem/', views.pay_item, name='payitems'),
    path('payment/', views.payment, name='payment-page'),
    path('payments/', views.payment_details, name='payment_details'),

]

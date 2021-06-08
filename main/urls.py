from django.urls import path
from . import views
from .views import *
from .views import (
    menuDetail,
    add_to_cart,
    get_cart_items,
    CartDeleteView,
    OrderDeleteView,
    order_details,
    add_reviews,
    order_delivery,
    payment,
)

app_name = "main"

urlpatterns = [
    # Home and dish url
    path('', views.home, name='home'),
    path('dishes/<slug>', views.menuDetail, name='dishes'),

    # cart urls
    path('add-to-order/<slug>/', views.add_to_cart, name='add-to-order'),
    path('cart/', views.get_cart_items, name='cart'),
    path('remove-from-cart/<int:pk>/',
         CartDeleteView.as_view(), name='remove-from-cart'),
    path('postReview', views.add_reviews, name='add_reviews'),
    # orders and delivery urls path
    path('order_details/', views.order_details, name='order_details'),
    path('order_delivery/', views.order_delivery, name='order_delivery'),
    path('remove-from-order/<int:pk>/',
         OrderDeleteView.as_view(), name='remove-from-order'),
    path('delivery_details/', views.delivery_details, name='delivery_details'),

    # views for payment
    path('payroll_registration/', views.payroll_reg, name='payroll_reg'),
    path('payitem/', views.pay_item, name='payitems'),
    path('payment/', views.payment, name='payment-page'),
    path('payments/', views.payment_details, name='payment_details'),



]

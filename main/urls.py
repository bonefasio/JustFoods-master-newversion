from django.urls import path, re_path
from . import views
from .views import *
from .views import (
    MenuListView,
    BreakfastListView,
    DinnerListView,
    LunchListView,
    menuDetail,
    add_to_cart,
    get_cart_items,
    order_item,
    CartDeleteView,
    SubscriptionDeleteView,
    OrderDeleteView,
    order_details,
    admin_view,
    item_list,
    pending_orders,
    ItemCreateView,
    ItemUpdateView,
    ItemDeleteView,
    update_status,
    add_reviews,
    order_delivery,
    payment,
)

app_name = "main"

urlpatterns = [
    # Home and dish url
    path('', MenuListView.as_view(), name='home'),
    path('dishes/<slug>', views.menuDetail, name='dishes'),

    # cart urls
    path('add-to-order/<slug>/', views.add_to_cart, name='add-to-order'),
    path('cart/', views.get_cart_items, name='cart'),
    path('remove-from-cart/<int:pk>/',
         CartDeleteView.as_view(), name='remove-from-cart'),

    # orders urls path
    path('ordered/', views.order_item, name='ordered'),
    path('order_details/', views.order_details, name='order_details'),
    path('order_delivery/', views.order_delivery, name='order_delivery'),
    path('remove-from-order/<int:pk>/',
         OrderDeleteView.as_view(), name='remove-from-order'),
    # views for payment
    path('payroll_registration/', views.payroll_reg, name='payroll_reg'),
    path('payitem/', views.pay_item, name='payitems'),
    path('payment/', views.payment, name='payment-page'),
    path('payments/', views.payment_details, name='payment_details'),
    path('payment_paypal/', views.payment_paypal, name='payment_paypal'),
    # views for custom meal
    path('custom_meal/', views.custom_meal, name='custom_meal'),
    # views for delivery
    path('delivery_details/', views.delivery_details, name='delivery_details'),

    # Meal Subscription
    path('subscriptionreg/<slug>', views.subscription_reg, name='subscription_reg'),
    path('subscribing/<slug>', views.subscriptionDetail, name='subscribing'),
    path('remove-from-subscription/<int:pk>/',
         SubscriptionDeleteView.as_view(), name='remove-from-subscription'),

    # Specials
    path('breakfast', BreakfastListView.as_view(), name='breakfast'),
    path('lunch/', DinnerListView.as_view(), name='lunch'),
    path('dinner/', LunchListView.as_view(), name='dinner'),

    # Cafeteria Staff Page
    path('admin_view/', views.admin_view, name='admin_view'),
    path('pending_orders/', views.pending_orders, name='pending_orders'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('update_status/<int:pk>', views.update_status, name='update_status'),
    path('postReview', views.add_reviews, name='add_reviews'),
    path('item_list/', views.item_list, name='item_list'),
    path('item/new/', ItemCreateView.as_view(), name='item-create'),
    path('item-update/<slug>/', ItemUpdateView.as_view(), name='item-update'),
    path('item-delete/<slug>/', ItemDeleteView.as_view(), name='item-delete'),
]

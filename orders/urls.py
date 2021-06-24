from django.urls import path, re_path
from . import views
from .views import *

app_name = "orders"

urlpatterns = [
    # cart urls
    path('dishes/<slug>', views.menuDetail, name='dishes'),
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

]

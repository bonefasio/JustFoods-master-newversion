from django.urls import path, re_path
from . import views
from mealsubscription.views import *


app_name = 'mealsubscription'

urlpatterns = [
    path('subscriptionreg/<slug>', views.subscription_reg, name='subscription_reg'),
    path('subscribing/<slug>', views.subscriptionDetail, name='subscribing'),
    path('remove-from-subscription/<int:pk>/',
         SubscriptionDeleteView.as_view(), name='remove-from-subscription'),
    path('custom_meal/', views.custom_meal, name='custom_meal'),

]

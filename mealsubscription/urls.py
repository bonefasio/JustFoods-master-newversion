from django.urls import path, re_path
from . import views


app_name = 'mealsubscription'

urlpatterns = [
    path('subscribing/<slug>', views.subscriptionDetail, name='subscribing'),
    path('subscriptionreg/<slug>', views.subscription_reg, name='subscription_reg'),

]

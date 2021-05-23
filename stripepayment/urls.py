from django.urls import path, re_path
from . import views

app_name = "stripepayment"

urlpatterns = [

    # stripe payment urls
    path('stripe', views.index, name="stripe"),
    path('charge/', views.charge, name="charge"),
    path('success/', views.successMsg, name="success"),
]

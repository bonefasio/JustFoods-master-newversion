from django.urls import path
from . import views

app_name = "stripepayment"

urlpatterns = [

    # stripe payment urls
    path('stripe/', views.index, name="index"),
    path('charge/', views.charge, name="charge"),
    path('success/', views.success, name="pay-success"),
]

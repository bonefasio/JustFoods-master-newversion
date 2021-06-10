from django.urls import path
from . import views
from .views import *

app_name = "main"

urlpatterns = [
    # Home and dish url
    path('', views.home, name='home'),
    path('dishes/<slug>', views.menuDetail, name='dishes'),
]

from django.urls import path
from . import views
from .views import *


app_name = "mealmenu"

urlpatterns = [
    # Specials
    path('breakfast', views.breakfast, name='breakfast'),
    path('lunch/', views.lunch, name='lunch'),
    path('dinner/', views.dinner, name='dinner'),
    path('custom_meal/', views.custom_meal, name='custom_meal'),
]
